
# <img width="48" height="48" src="../../icons/icon_tag_oclSVG.svg" /> OpenCL
## File name: [**`cl_flam3.cl`**](cl_flam3.cl)
## Houdini version: H20.5 and up
### Description:
Implementation of the algorithm using OpenCL for high performance.<br>
It run billions of iterations per second in Houdini Sop.<br>

_This file include everything_:<br>
- variations' functions
- variations' dispatch
- RNG noises
- weighted probabilities
- the chaos game
- CDF sampling
- kernels
- everything else...

<br>

To maximize performance and since the data is already on the GPU<br>
the **FF**(_finalXform_) run as a separate kernel in its own OpenCL node.<br>

<br>

## Note on the OpenCL implementation

* The OpenCL implementation used the CVEX code as its reference starting point, as a significant amount of effort had already been invested in porting the original Flam3 mathematics to FLAM3H™.

* To take advantage of GPU parallelism, most, if not all, variations have been adapted to be GPU-friendly. Where possible, they have been made branchless and include both a ground-truth implementation and a performance-oriented variant that relies exclusively on OpenCL `native_*()` functions. Many mathematical blocks have also been rewritten using lighter-weight approximations better suited to GPU execution.

* The CVEX codebase could now benefit from the knowledge gained during the development of the GPU implementation. However, it has intentionally been left unchanged to mirror the original Flam3 codebase as closely as possible and serve as the sole reference for correctness. This ensures that the GPU implementation always has a reliable ground truth against which it can be validated.

* If and when SideFX expands the capabilities of the CVEX language, I may revisit the implementation and attempt a rewrite to improve performance and, hopefully, overcome some of the current limitations of CVEX.

<br>
<br>
<br>
<br>

# Hardware Performance Profile  

**FLAM3H™ OpenCL Kernel:** cl_flam3  
**Target Architecture:** NVIDIA Ada Lovelace (`sm_89` / RTX 40-Series)  
**Tested On:** NVIDIA GeForce RTX 4090  
**NVIDIA Driver Version:** 610.88  
**Compilation Context:** Houdini OpenCL Runtime Code Cache  

---

<br>
<br>

## Summary of PTXAS Compiler Report

| Hardware Resource | Metric Value | Description |
| :--- | :--- | :--- |
| **Global Memory (`gmem`)** | **0** bytes | Statically allocated global memory usage. |
| **Stack Frame** | **0** bytes | Per-thread stack memory allocation. |
| **Spill Stores / Loads** | **0** bytes / **0** bytes | Register spills caused by register pressure. |
| **Registers Used** | **50** registers | Number of 32-bit registers allocated per thread. |
| **Execution Barriers** | **1** barrier | Number of synchronization barrier instructions. |
| **Shared Memory (`smem`)** | **16,432** bytes (~16.4 KB) | Shared memory allocated per thread block. |
| **Constant Memory 0 (`cmem[0]`)** | **872** bytes | Constant memory for kernel parameters and compiler-managed data. |
| **Constant Memory 2 (`cmem[2]`)** | **4,120** bytes (~4.1 KB) | Constant memory for read-only data. |

---

<br>
<br>

## Summary of SASS Hardware Metrics

| Instruction Class | Hardware Functions | Assembly Count | Description |
| :--- | :--- | :--- | :--- |
| **ALU Core Math** | `FMA`, `FMUL`, `FADD` | **15,931** | Floating-point arithmetic operations. |
| **Special Functions** | `MUFU` | **3,117** | Transcendental math functions (e.g., `sin`, `cos`, `log`). |
| **Control Flow** | `BRA`, `BRX` | **2,482** | Branching and loop control instructions. |
| **Integer & Indexing** | `IADD3`, `IMAD` | **849** | Integer arithmetic and address calculations. |
| **Shared Memory Cache** | `LDS`, `STS` | **465** | Shared memory load and store operations. |
| **Global Memory Bus** | `LDG`, `STG` | **72** | Global memory load and store operations. |
| **Dependency Management** | `DEPBAR`, `LGWR` | **0** | Instruction dependency management operations. |
| **Thread Synchronization** | `BAR.SYNC` | **1** | Thread block synchronization barrier. |

```rust
  F3H_sass_output.txt:1327:        /*2940*/                   IADD3 R0, R0, c[0x0][0x94], RZ ;
        /* 0x0000250000007a10 */
  F3H_sass_output.txt:1328:
        /* 0x000fc60007ffe0ff */
> F3H_sass_output.txt:1329:        /*2950*/                   BAR.SYNC.DEFER_BLOCKING 0x0 ;
        /* 0x0000000000007b1d */
  F3H_sass_output.txt:1330:
        /* 0x000fe40000010000 */
  F3H_sass_output.txt:1331:        /*2960*/                   IMAD R0, R3, c[0x0][0x0], R0 ;
        /* 0x0000000003007a24 */
```
---
