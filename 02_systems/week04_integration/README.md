# Week 4 lab: TCP loopback to bounded frame workers

This integration lab turns the in-memory frame producer into a fake sensor
process connected through a real TCP stream. It combines process/resource
ownership, byte representation, the week 3 queue, worker shutdown, and measured
backpressure without introducing a camera or ML framework yet.

```text
fake sensor process -> TCP loopback -> frame decoder -> bounded queue
                                                     -> worker threads
                                                     -> ordered results/metrics
```

## Prepare

**Required concepts**

- Read the overview and data-transfer sections of [Beej's Guide to Network
  Programming](https://beej.us/guide/bgnet/) and the relevant
  [`send(2)`](https://man7.org/linux/man-pages/man2/send.2.html) and
  [`recv(2)`](https://man7.org/linux/man-pages/man2/recv.2.html) contracts.
  Draw client, server, IP address, listening port, accepted connection, and each
  owning process. TCP is an ordered byte stream: one `recv()` is not one
  application message, and one `send()` need not accept the full request.
  Write a two-column TCP/UDP comparison covering connection setup, ordering,
  reliability, datagram boundaries, and which framing/retry duties remain with
  the application. TCP is required for the implementation; UDP is conceptual.
- Read Microsoft's [Winsock client/server
  introduction](https://learn.microsoft.com/en-us/windows/win32/winsock/getting-started-with-winsock)
  and [network byte-order
  functions](https://learn.microsoft.com/en-us/windows/win32/api/winsock/nf-winsock-htonl).
  Explain why copying a native C++ `Frame` object directly onto the wire would
  depend on padding, field widths, and host byte order.
- Revisit OSTEP [Chapter 30: Condition
  Variables](https://pages.cs.wisc.edu/~remzi/OSTEP/threads-cv.pdf) and C++ Core
  Guidelines [CP.20, CP.23, and
  CP.42](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#Rconc-wait).
  Add TCP receive, clean EOF, truncated EOF, and peer error to the existing
  queue/worker shutdown diagram.

**Ready-to-code check**

Without a source open, answer: if a sender makes two `send()` calls containing
two frames, what may the receiver's next three `recv()` calls return? Then state
how a length prefix lets the decoder recover message boundaries and which limit
must be checked before allocating memory.

**API references while coding**

- Trace `net::TcpConnection::send_some` and `recv_some` in the supplied
  `infrastructure/tcp_socket.cpp` once. The wrapper owns Winsock/POSIX setup and
  handles; it does not change stream semantics.
- Use the Microsoft [`std::thread`
  reference](https://learn.microsoft.com/en-us/cpp/standard-library/thread-class?view=msvc-170)
  to verify ownership, `joinable`, and `join` contracts. Use the standard
  [`<exception>` facilities](https://learn.microsoft.com/en-us/cpp/standard-library/exception?view=msvc-170)
  when transporting the first worker/receiver failure to its owner.

**Optional / after the first attempt**

- Read the current TCP specification, [RFC
  9293](https://www.rfc-editor.org/rfc/rfc9293.html), only to resolve a concrete
  stream, close, or reset question. TCP reliability does not supply application
  framing or an application-level completeness policy.
- Compare the blocking queue with GStreamer's production [`appsink` queue
  controls](https://gstreamer.freedesktop.org/documentation/app/appsink.html).
- A UDP probe is optional after the required TCP lab; it is not a replacement
  for the required conceptual comparison, framing, or partial-I/O work.

## Supplied infrastructure versus learner work

The supplied move-only `TcpConnection` and `TcpListener` provide real IPv4
loopback sockets on Winsock and POSIX. They expose `send_some`, `recv_some`,
`shutdown_write`, `accept`, and port-zero binding. Native handles never appear in
the learner-facing API.

You implement the application-level behavior:

1. finish the original `process_frames` bounded worker checkpoint;
2. implement `encode_frame`, incremental `FrameDecoder`, and `write_all` in
   `starter/frame_protocol.cpp`;
3. implement `receive_and_process_frames` in `starter/tcp_pipeline.cpp` so
   decoded frames enter the bounded queue as they arrive.

Do not read the entire connection into a vector and call `process_frames`
afterward. A full work queue must stop the receiver from calling `recv_some`, so
pressure can propagate into the finite kernel receive/send buffers and
eventually slow the producer.

## Wire contract

Every unsigned field uses big-endian (network) byte order:

| Bytes | Field |
|---:|---|
| 4 | body byte length |
| 8 | frame sequence |
| 4 | sample count |
| `4 * sample_count` | signed 32-bit samples |

The body length is exactly `12 + 4 * sample_count`. Reject undersized bodies,
count/length disagreement, arithmetic overflow, and bodies above the configured
limit. Do not serialize object memory, type-pun through unrelated pointers, or
interpret a partial prefix.

Clean EOF at a frame boundary ends input. EOF during a prefix or body is a
`ProtocolError`. On clean EOF, close the queue, drain queued frames, join all
workers, and return ordered results. On protocol, socket, or worker failure,
unblock all stages, join owned threads, then propagate the first failure.

## Build and focused checks

```text
cmake --preset default
cmake --build --preset default
ctest --test-dir build -C Debug -R systems_week04_socket --output-on-failure
ctest --test-dir build -C Debug -R systems_week04_protocol --output-on-failure
ctest --test-dir build -C Debug -R systems_week04_tcp --output-on-failure
```

The socket-support test should pass before learner work. Protocol and TCP
pipeline tests are executable specifications and remain red until their
`LEARNER TODO`s are implemented. They cover exact byte order, every split point,
coalesced frames, deterministic short writes, scripted one-byte reads, clean
half-close, and mid-frame disconnect. CTest bounds blocking tests so a shutdown
bug becomes a failure rather than an endless run.

## Run two real processes

After the learner targets pass, start the receiver in one terminal:

```text
build\Debug\systems_tcp_receiver.exe 40404 2 2 17
```

Then start the fake sensor in another:

```text
build\Debug\systems_fake_sensor.exe 40404 100 4096 3
```

On a single-config Linux/WSL build, use `./build/systems_tcp_receiver` and
`./build/systems_fake_sensor`. The last sensor argument shown above limits each
`send_some` call to three bytes; it does not change the decoded frames. Port zero
is supported by the receiver and prints the assigned port for collision-free
manual runs.

## Required experiments

1. Run maximum send chunks 1, 3, 64, and unlimited, plus receive chunks 1, 17,
   and 4096. Results must remain identical. Log bytes, calls, and the distinction
   between an API call boundary, a TCP segment, and a frame boundary.
2. While both processes are connected, inspect the local connection. On
   Linux/WSL use `ss -tnp 'sport = :40404 or dport = :40404'`. If available,
   capture only this loopback port with
   `sudo tcpdump -i lo -nn 'tcp port 40404'`; optionally trace calls with
   `strace -f -e trace=network`. Identify listen versus established endpoints,
   Send-Q/Recv-Q, handshake, payload, and FIN. Do not infer one frame per packet.
   On Windows, `Get-NetTCPConnection -LocalPort 40404` provides a smaller state
   observation route.
3. Temporarily add a 5 ms worker delay, use queue capacity 1, and send a burst
   much larger than the socket buffers. Compare capacities 1, 4, and 16. Record
   maximum queue depth with temporary instrumentation, sender elapsed time, and
   socket queue observations. Explain the causal chain from slow worker to full
   bounded queue to paused receiver to kernel buffers to blocked/short sender.
   Restore the artificial delay afterward.
4. Append the optional `DISCONNECT_AFTER_BYTES` value after `MAX_SEND_CHUNK`
   (the fake sensor's fifth user argument) to disappear in the middle of a
   prefix, in the middle of a body, and exactly at a frame boundary. Explain
   which cases are
   protocol errors, why EOF on a boundary can still be valid after producer
   disappearance, and what an explicit end message would change.
5. Benchmark only representative worker/capacity pairs `(1,1)`, `(2,4)`, and
   `(4,16)` for two payload sizes. Warm up and report the median of at least five
   runs. This replaces the old 16-cell matrix so networking depth does not
   become duplicate benchmark volume.

An OS receive timeout limits one blocking operation; it is not automatically a
deadline for a complete frame or the whole connection. The CTest timeout is an
outer test-hang guard, not the production timeout policy. Timed/nonblocking I/O
is a design exercise here, not a required event-loop implementation.

## Platform contract

- Windows uses supplied Winsock setup/cleanup and links the Windows SDK's
  `Ws2_32`; no third-party networking library is required.
- Linux/WSL uses POSIX sockets. The supplied sender suppresses process-killing
  `SIGPIPE` where the platform exposes `MSG_NOSIGNAL`.
- Required code is IPv4 loopback (`127.0.0.1`) only. DNS, IPv6, TLS,
  nonblocking multiplexing, reconnect protocols, and remote-host security are
  intentionally out of scope.
- ThreadSanitizer is Linux/WSL-only in this course. Complete the Week 3 race
  clinic before deciding how shared network-pipeline metrics are synchronized.

## Phase 0 systems exit

Reimplement a small `BoundedQueue<int>` and the four-byte framing state machine
from memory. Then explain the complete path using producer process, TCP byte
stream, decoder, queue, workers, ordered result slots, clean/error close, and
join. You are done when you can explain TCP stream semantics, partial I/O, byte
order, framing, disconnect handling, the relevant TCP/UDP distinction, and how
bounded-queue pressure reaches the producer without claiming that TCP preserves
application messages.
