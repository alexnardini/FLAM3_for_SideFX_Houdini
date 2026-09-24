
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


<br/>
<br/>
<br/>
<br/>
<br/>
<br/>

# OpenCL Hardware Performance Profile

<br/>
<br/>

## <img width="48" height="48" src="../../icons/icon_tag_oclSVG.svg" /> OpenCL Kernel: <u>**cl_flam3**</u> 

**Target Architecture:** NVIDIA Ada Lovelace (`sm_89` / RTX 40-Series)  
**Tested On:** NVIDIA GeForce RTX 4090  
**NVIDIA Driver Version:** 580.97  
**Compilation Context:** Houdini OpenCL Runtime Code Cache  

---

**Work-Group size:** 256  

---

<br>

## <img width="24" height="24" src="../../icons/icon_tag_oclSVG.svg" /> Summary of PTXAS Compiler Report

| Hardware Resource | Metric Value | Description |
| :--- | :--- | :--- |
| **Global Memory (`gmem`)** | **0** bytes | Statically allocated global memory usage. |
| **Stack Frame** | **0** bytes | Per-thread stack memory allocation. |
| **Spill Stores / Loads** | **0** bytes / **0** bytes | Register spills caused by register pressure. |
| **Registers Used** | **48** registers | Number of 32-bit registers allocated per thread. |
| **Execution Barriers** | **1** barrier | Number of synchronization barrier instructions. |
| **Shared Memory (`smem`)** | **16,400** bytes (16.4 KB) | Shared memory allocated per thread block. |
| **Constant Memory 0 (`cmem[0]`)** | **872** bytes | Constant memory for kernel parameters and compiler-managed data. |
| **Constant Memory 2 (`cmem[2]`)** | **4,120** bytes (~4.1 KB) | Constant memory for read-only data. |

---

<br>

## <img width="24" height="24" src="../../icons/icon_tag_oclSVG.svg" /> Summary of SASS Hardware Metrics

| Instruction Class | Hardware Functions | Assembly Count | Description |
| :--- | :--- | :--- | :--- |
| **ALU Core Math** | `FMA`, `FMUL`, `FADD` | **15,960** | Floating-point arithmetic operations. |
| **Special Functions** | `MUFU` | **3,117** | Transcendental math functions (e.g., `sin`, `cos`, `log`). |
| **Control Flow** | `BRA`, `BRX` | **2,482** | Branching and loop control instructions. |
| **LOP3.LUT instructions** | `LOP3.LUT` | **2,709** | 3-input programmable bitwise logic instructions. |
| **Integer & Indexing** | `IADD3`, `IMAD` | **844** | Integer arithmetic and address calculations. |
| **Shared Memory Cache** | `LDS`, `STS` | **454** | Shared memory load and store operations. |
| **Global Memory Bus** | `LDG`, `STG` | **72** | Global memory load and store operations. |
| **Thread Synchronization** | `BAR.SYNC` | **1** | Thread block synchronization barrier. |
| **Dependency Management** | `DEPBAR`, `LGWR` | **0** | Instruction dependency management operations. |

---

<br/>
<br/>
<br/>
<br/>

## <img width="48" height="48" src="../../icons/icon_tag_oclSVG.svg" /> OpenCL Kernel: <u>**cl_flam3_ff**</u>

**Target Architecture:** NVIDIA Ada Lovelace (`sm_89` / RTX 40-Series)  
**Tested On:** NVIDIA GeForce RTX 4090  
**NVIDIA Driver Version:** 580.97  
**Compilation Context:** Houdini OpenCL Runtime Code Cache  

---

**Work-Group size:** 256  

---

<br>

## <img width="24" height="24" src="../../icons/icon_tag_oclSVG.svg" /> Summary of PTXAS Compiler Report

| Hardware Resource | Metric Value | Description |
| :--- | :--- | :--- |
| **Global Memory (`gmem`)** | **0** bytes | Statically allocated global memory usage. |
| **Stack Frame** | **0** bytes | Per-thread stack memory allocation. |
| **Spill Stores / Loads** | **0** bytes / **0** bytes | Register spills caused by register pressure. |
| **Registers Used** | **40** registers | Number of 32-bit registers allocated per thread. |
| **Execution Barriers** | **1** barrier | Number of synchronization barrier instructions. |
| **Shared Memory (`smem`)** | **1,248** bytes (~1.2 KB) | Shared memory allocated per thread block. |
| **Constant Memory 0 (`cmem[0]`)** | **624** bytes | Constant memory for kernel parameters and compiler-managed data. |
| **Constant Memory 2 (`cmem[2]`)** | **2,960** bytes (~2.9 KB) | Constant memory for read-only data. |

---

<br>

## <img width="24" height="24" src="../../icons/icon_tag_oclSVG.svg" /> Summary of SASS Hardware Metrics

| Instruction Class | Hardware Functions | Assembly Count | Description |
| :--- | :--- | :--- | :--- |
| **ALU Core Math** | `FMA`, `FMUL`, `FADD` | **11,384** | Floating-point arithmetic operations. |
| **Special Functions** | `MUFU` | **2,225** | Transcendental math functions (e.g., `sin`, `cos`, `log`). |
| **Control Flow** | `BRA`, `BRX` | **1,771** | Branching and loop control instructions. |
| **LOP3.LUT instructions** | `LOP3.LUT` | **1,876** | 3-input programmable bitwise logic instructions. |
| **Integer & Indexing** | `IADD3`, `IMAD` | **568** | Integer arithmetic and address calculations. |
| **Shared Memory Cache** | `LDS`, `STS` | **304** | Shared memory load and store operations. |
| **Global Memory Bus** | `LDG`, `STG` | **40** | Global memory load and store operations. |
| **Thread Synchronization** | `BAR.SYNC` | **1** | Thread block synchronization barrier. |
| **Dependency Management** | `DEPBAR`, `LGWR` | **0** | Instruction dependency management operations. |

---

<br/>
<br/>
<br/>
<br/>

_Copyright (c) 2021 F stands for liFe_<br/>
