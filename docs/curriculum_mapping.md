# Curriculum Mapping

The supplied curriculum mixed a weekly syllabus, a resource library, hardware
guidance, career positioning, and a capstone specification. Its numbered sections
map as follows:

| Source section | Repository translation |
|---|---|
| 0. Hardware assignment | `SETUP.md`, `docs/compatibility.md`, CUDA machine-note templates |
| 1. Rules of engagement | `LEARNING_GUIDE.md`, progress logs, chapter completion gates |
| 2. Study method | Red-test/recall workflow plus weekly exercise sheets |
| 3. Resource library | `docs/resources.md` and focused references inside each lab |
| 4. Week-by-week syllabus | `COURSE_MAP.md` and eight numbered chapter directories |
| 5. Definition of done | Phase gates in `COURSE_MAP.md` and the application gate in Chapter 08 |
| 6. Resume targets | `08_interviews/evidence_matrix.template.md` and walkthrough drill |
| 7. What not to do | Scope guardrails in the capstone and learning guide |
| 8. Calendar | `scripts/make_schedule.py` |
| 9. Link dump | Curated primary links in `docs/resources.md` and `docs/compatibility.md` |

The four learning phases become executable chapters:

| Source idea | Repository location | Translation |
|---|---|---|
| Phase 0 “un-rust” | `01_cpp_fluency`, `02_systems` | Recall drills, C++17 starters, behavior tests, applied OS experiments |
| Phase 1 ML math + PyTorch | `03_ml_fundamentals`, `04_computer_vision` | Derivations become numerical checks; notes become implementations |
| Phase 2 CUDA | `05_cuda`, `06_gpu_optimization` | Kernels, CPU oracles, timing harnesses, profiler worksheets |
| Phase 3 detect-track | `07_edge_detect_track` | Gated project from data audit through edge deployment |
| Phase 4 applications | `08_interviews` | Timed practice, design rubrics, and evidence-based resume prompts |

The source's dates and vendor model names are treated as suggestions. Volatile
compatibility facts live in `docs/compatibility.md` so the conceptual exercises do
not have to change every time a toolchain does.

External assignments (for example CS231n or GPU Puzzles) remain optional extension
work. This repository does not redistribute their content or solutions.
