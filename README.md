# Interactive Optical Fibre Simulator 

A computational instrumentation dashboard built using Python and Tkinter. This tool simulates wave propagation vectors, refractive boundaries, and signal attenuation metrics within optical waveguides.

##  Core Engineering & Physics Features
* **Ray Optics Engine:** Real-time calculation of Numerical Aperture (NA), Critical Angles, and Maximum Acceptance Envelopes.
* **Wave Dynamics Modeler:** Automates V-number evaluation to track Single-Mode vs. Multi-Mode fiber transitions.
* **Link Budget Tracker:** Computes logarithmic signal attenuation and power degradation curves over varying geographic distances ($L$).
* **Data Logging Integration:** Automated CSV transaction ledger to track data parameters across multiple execution trials.

## Technical Architecture & Dependencies
* **GUI Engine:** Python Tkinter (Object-Oriented structural architecture)
* **Numerical Computations:** NumPy 
* **Data Visualization Canvas:** Matplotlib (Embedded FigureCanvasTkAgg interface)
