import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import csv
import os
from datetime import datetime
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


# CSV CONFIGURATION
CSV_FILE = "optical_fibre_trials.csv"
CSV_COLUMNS = [
    "Trial No",
    "Date",
    "Time",
    "Core Refractive Index (n1)",
    "Clad Refractive Index (n2)",
    "Core Diameter (µm)",
    "Fibre Length (km)",
    "Input Power (mW)",
    "Attenuation (dB/km)",
    "Launch Angle (degree)",
    "Wavelength (nm)",
    "Numerical Aperture",
    "Critical Angle",
    "Acceptance Angle",
    "V-number",
    "Number of Modes",
    "Output Power (mW)"
]
# MAIN APPLICATION
class OpticalFibreSimulator:

    def __init__(self, root):

        self.root = root
        # WINDOW
        self.root.title(
            "Interactive Optical Fibre Simulator"
        )
        self.root.geometry("1500x950")
        self.root.minsize(1200, 750)
        #COLOUR THEME
        self.bg = "#080D1A"
        self.panel = "#101827"
        self.panel2 = "#172235"

        self.text = "#F8FAFC"
        self.subtext = "#94A3B8"

        self.cyan = "#22D3EE"
        self.blue = "#3B82F6"
        self.purple = "#A855F7"
        self.green = "#22C55E"
        self.orange = "#F59E0B"
        self.red = "#EF4444"

        self.root.configure(
            bg=self.bg
        )
        # PHYSICAL PARAMETERS
        self.core_index = tk.DoubleVar(
            value=1.48
        )
        self.cladding_index = tk.DoubleVar(
            value=1.46
        )
        # NEW PARAMETER
        self.core_diameter = tk.DoubleVar(
            value=50
        )
        self.fibre_length = tk.DoubleVar(
            value=20
        )
        self.input_power = tk.DoubleVar(
            value=10
        )
        self.attenuation = tk.DoubleVar(
            value=0.20
        )
        self.launch_angle = tk.DoubleVar(
            value=10
        )
        self.wavelength = tk.IntVar(
            value=1550
        )
        # ROOT GRID
        self.root.grid_columnconfigure(
            0,
            weight=0
        )
        self.root.grid_columnconfigure(
            1,
            weight=1
        )
        self.root.grid_rowconfigure(
            0,
            weight=1
        )
        # LEFT CONTROL PANEL
        self.left_panel = tk.Frame(
            self.root,
            bg=self.panel,
            width=330
        )
        self.left_panel.grid(
            row=0,
            column=0,
            sticky="ns"
        )
        self.left_panel.grid_propagate(
            False
        )
        # RIGHT PANEL
        self.right_panel = tk.Frame(
            self.root,
            bg=self.bg
        )
        self.right_panel.grid(
            row=0,
            column=1,
            sticky="nsew"
        )
        self.right_panel.grid_rowconfigure(
            1,
            weight=3
        )
        self.right_panel.grid_rowconfigure(
            2,
            weight=2
        )
        self.right_panel.grid_columnconfigure(
            0,
            weight=1
        )
        # BUILD INTERFACE
        self.create_left_panel()
        self.create_visualization()
        self.create_trial_history()
        # CSV
        self.initialize_csv()
        # LOAD PREVIOUS TRIALS
        self.load_trials()
        # INITIAL SIMULATION
        self.simulate(
            save_trial=False
        )
    # LEFT PANEL
    def create_left_panel(self):
        title = tk.Label(
            self.left_panel,
            text="OPTICAL FIBRE\nSIMULATOR",
            font=("Segoe UI", 20, "bold"),
            fg=self.cyan,
            bg=self.panel,
            justify="left"
        )
        title.pack(
            anchor="w",
            padx=20,
            pady=(20, 3)
        )
        subtitle = tk.Label(
            self.left_panel,
            text="Interactive Physics Simulation",
            font=("Segoe UI", 9),
            fg=self.subtext,
            bg=self.panel
        )
        subtitle.pack(
            anchor="w",
            padx=20,
            pady=(0, 15)
        )
        # CORE REFRACTIVE INDEX
        self.create_slider(
            "Core refractive index (n₁)",
            self.core_index,
            1.40,
            1.60,
            0.001
        )
        # CLADDING REFRACTIVE INDEX
        self.create_slider(
            "Cladding refractive index (n₂)",
            self.cladding_index,
            1.30,
            1.59,
            0.001
        )
        # CORE DIAMETER
        self.create_slider(
            "Core diameter (µm)",
            self.core_diameter,
            1,
            200,
            1
        )
        # FIBRE LENGTH
        self.create_slider(
            "Fibre length (km)",
            self.fibre_length,
            1,
            100,
            1
        )
        # INPUT POWER
        self.create_slider(
            "Input power (mW)",
            self.input_power,
            1,
            100,
            1
        )
        # ATTENUATION
        self.create_slider(
            "Attenuation (dB/km)",
            self.attenuation,
            0,
            2,
            0.05
        )
        # LAUNCH ANGLE
        self.create_slider(
            "Launch angle (degree)",
            self.launch_angle,
            0,
            30,
            0.5
        )
        # WAVELENGTH
        tk.Label(
            self.left_panel,
            text="Wavelength (nm)",
            font=("Segoe UI", 9, "bold"),
            fg=self.text,
            bg=self.panel
        ).pack(
            anchor="w",
            padx=20,
            pady=(8, 4)
        )
        wavelength_box = ttk.Combobox(
            self.left_panel,
            textvariable=self.wavelength,
            values=[
                450,
                650,
                850,
                1064,
                1310,
                1550
            ],
            state="readonly",
            width=20
        )
        wavelength_box.pack(
            anchor="w",
            padx=20
        )
        wavelength_box.bind(
            "<<ComboboxSelected>>",
            lambda event:
            self.simulate(
                save_trial=False
            )
        )
        # RUN BUTTON
        run_button = tk.Button(
            self.left_panel,
            text="▶  RUN SIMULATION",
            command=lambda:
            self.simulate(
                save_trial=True
            ),
            font=("Segoe UI", 10, "bold"),
            fg="white",
            bg=self.purple,
            activeforeground="white",
            activebackground=self.blue,
            relief="flat",
            bd=0,
            cursor="hand2",
            padx=10,
            pady=10
        )
        run_button.pack(
            fill="x",
            padx=20,
            pady=15
        )
        # RESULTS TITLE
        tk.Label(
            self.left_panel,
            text="SIMULATION RESULTS",
            font=("Segoe UI", 11, "bold"),
            fg=self.cyan,
            bg=self.panel
        ).pack(
            anchor="w",
            padx=20,
            pady=(0, 8)
        )
        # RESULT BOXES
        self.na_label = self.create_result(
            "Numerical Aperture"
        )
        self.critical_label = self.create_result(
            "Critical Angle"
        )
        self.acceptance_label = self.create_result(
            "Acceptance Angle"
        )
        self.v_number_label = self.create_result(
            "V-number"
        )
        self.modes_label = self.create_result(
            "Number of Modes"
        )
        self.output_label = self.create_result(
            "Output Power"
        )
        self.loss_label = self.create_result(
            "Total Loss"
        )
        # STATUS
        self.status_label = tk.Label(
            self.left_panel,
            text="● Ready",
            font=("Segoe UI", 10, "bold"),
            fg=self.green,
            bg=self.panel
        )
        self.status_label.pack(
            anchor="w",
            padx=20,
            pady=12
        )
    # CREATE SLIDER
    def create_slider(
        self,
        label,
        variable,
        minimum,
        maximum,
        resolution
    ):
        frame = tk.Frame(
            self.left_panel,
            bg=self.panel
        )
        frame.pack(
            fill="x",
            padx=20,
            pady=2
        )
        label_frame = tk.Frame(
            frame,
            bg=self.panel
        )
        label_frame.pack(
            fill="x"
        )
        tk.Label(
            label_frame,
            text=label,
            font=("Segoe UI", 9),
            fg=self.text,
            bg=self.panel
        ).pack(
            side="left"
        )
        tk.Label(
            label_frame,
            textvariable=variable,
            font=("Segoe UI", 9, "bold"),
            fg=self.cyan,
            bg=self.panel
        ).pack(
            side="right"
        )
        slider = tk.Scale(
            frame,
            variable=variable,
            from_=minimum,
            to=maximum,
            resolution=resolution,
            orient=tk.HORIZONTAL,
            length=250,
            bg=self.panel,
            fg=self.cyan,
            troughcolor=self.panel2,
            highlightthickness=0,
            activebackground=self.cyan,
            sliderrelief="flat",
            showvalue=False
        )
        slider.pack(
            fill="x"
        )
        slider.bind(
            "<ButtonRelease-1>",
            lambda event:
            self.simulate(
                save_trial=False
            )
        )
    # RESULT BOX
    def create_result(
        self,
        name
    ):
        frame = tk.Frame(
            self.left_panel,
            bg=self.panel2
        )
        frame.pack(
            fill="x",
            padx=20,
            pady=2
        )
        label = tk.Label(
            frame,
            text=f"{name}: --",
            font=("Segoe UI", 9),
            fg=self.text,
            bg=self.panel2,
            anchor="w"
        )
        label.pack(
            padx=10,
            pady=5,
            fill="x"
        )
        return label
    # VISUALIZATION
    def create_visualization(self):
        title = tk.Label(
            self.right_panel,
            text="LIGHT PROPAGATION & OPTICAL POWER",
            font=("Segoe UI", 17, "bold"),
            fg=self.text,
            bg=self.bg
        )
        title.grid(
            row=0,
            column=0,
            sticky="w",
            padx=20,
            pady=(15, 5)
        )
        # FIGURE
        self.figure = Figure(
            figsize=(10, 7),
            dpi=100,
            facecolor=self.bg
        )
        self.ax1 = self.figure.add_subplot(
            211
        )
        self.ax2 = self.figure.add_subplot(
            212
        )
        # CANVAS
        self.canvas = FigureCanvasTkAgg(
            self.figure,
            master=self.right_panel
        )
        self.canvas.get_tk_widget().grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=15,
            pady=5
        )
    # TRIAL HISTORY
    def create_trial_history(self):
        frame = tk.Frame(
            self.right_panel,
            bg=self.panel
        )
        frame.grid(
            row=2,
            column=0,
            sticky="nsew",
            padx=15,
            pady=10
        )
        frame.grid_rowconfigure(
            1,
            weight=1
        )
        frame.grid_columnconfigure(
            0,
            weight=1
        )
        # TITLE
        tk.Label(
            frame,
            text="TRIAL HISTORY / CSV DATABASE",
            font=("Segoe UI", 12, "bold"),
            fg=self.cyan,
            bg=self.panel
        ).grid(
            row=0,
            column=0,
            sticky="w",
            padx=12,
            pady=7
        )
        # TABLE
        table_frame = tk.Frame(
            frame,
            bg=self.panel
        )
        table_frame.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=10
        )
        table_frame.grid_rowconfigure(
            0,
            weight=1
        )
        table_frame.grid_columnconfigure(
            0,
            weight=1
        )
        self.tree = ttk.Treeview(
            table_frame,
            columns=CSV_COLUMNS,
            show="headings",
            selectmode="extended"
        )
        # HEADINGS
        for column in CSV_COLUMNS:
            self.tree.heading(
                column,
                text=column
            )
            self.tree.column(
                column,
                width=125,
                minwidth=100,
                anchor="center"
            )
        # SPECIAL COLUMN WIDTHS
        self.tree.column(
            "Trial No",
            width=70
        )
        self.tree.column(
            "Date",
            width=100
        )
        self.tree.column(
            "Time",
            width=90
        )
        self.tree.column(
            "Core Diameter (µm)",
            width=120
        )
        self.tree.column(
            "Wavelength (nm)",
            width=110
        )
        self.tree.column(
            "Number of Modes",
            width=110
        )
        # SCROLLBARS
        vertical_scroll = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.tree.yview
        )
        horizontal_scroll = ttk.Scrollbar(
            table_frame,
            orient="horizontal",
            command=self.tree.xview
        )
        self.tree.configure(
            yscrollcommand=vertical_scroll.set,
            xscrollcommand=horizontal_scroll.set
        )
        self.tree.grid(
            row=0,
            column=0,
            sticky="nsew"
        )
        vertical_scroll.grid(
            row=0,
            column=1,
            sticky="ns"
        )
        horizontal_scroll.grid(
            row=1,
            column=0,
            sticky="ew"
        )
        # BUTTONS
        button_frame = tk.Frame(
            frame,
            bg=self.panel
        )
        button_frame.grid(
            row=2,
            column=0,
            sticky="w",
            padx=10,
            pady=7
        )
        # DELETE SELECTED
        delete_button = tk.Button(
            button_frame,
            text="🗑 Delete Selected Trial",
            command=self.delete_selected_trials,
            font=("Segoe UI", 9, "bold"),
            fg="white",
            bg=self.red,
            activebackground="#B91C1C",
            relief="flat",
            cursor="hand2",
            padx=12,
            pady=7
        )
        delete_button.pack(
            side="left",
            padx=(0, 8)
        )
        # DELETE ALL
        delete_all_button = tk.Button(
            button_frame,
            text="Delete All Trials",
            command=self.delete_all_trials,
            font=("Segoe UI", 9, "bold"),
            fg="white",
            bg="#7F1D1D",
            activebackground=self.red,
            relief="flat",
            cursor="hand2",
            padx=12,
            pady=7
        )
        delete_all_button.pack(
            side="left"
        )
    # INITIALIZE CSV
    def initialize_csv(self):
        if not os.path.exists(CSV_FILE):
            with open(
                CSV_FILE,
                "w",
                newline="",
                encoding="utf-8"
            ) as file:
                writer = csv.DictWriter(
                    file,
                    fieldnames=CSV_COLUMNS
                )
                writer.writeheader()
    # GET NEXT TRIAL NUMBER
    def get_next_trial_number(self):
        if not os.path.exists(CSV_FILE):
            return 1
        try:
            with open(
                CSV_FILE,
                "r",
                newline="",
                encoding="utf-8"
            ) as file:
                reader = csv.DictReader(
                    file
                )
                numbers = []
                for row in reader:
                    try:
                        numbers.append(
                            int(
                                row["Trial No"]
                            )
                        )
                    except (
                        ValueError,
                        TypeError
                    ):
                        pass
                if numbers:
                    return max(numbers) + 1
        except Exception:
            pass
        return 1
    # SAVE TRIAL
    def save_trial(
        self,
        NA,
        critical_angle,
        acceptance_angle,
        v_number,
        number_of_modes,
        output_power
    ):
        now = datetime.now()
        trial_number = (
            self.get_next_trial_number()
        )
        row = {
            "Trial No":
                trial_number,
            "Date":
                now.strftime(
                    "%Y-%m-%d"
                ),
            "Time":
                now.strftime(
                    "%H:%M:%S"
                ),
            "Core Refractive Index (n1)":
                f"{self.core_index.get():.3f}",
            "Clad Refractive Index (n2)":
                f"{self.cladding_index.get():.3f}",
            "Core Diameter (µm)":
                f"{self.core_diameter.get():.2f}",
            "Fibre Length (km)":
                f"{self.fibre_length.get():.2f}",
            "Input Power (mW)":
                f"{self.input_power.get():.3f}",
            "Attenuation (dB/km)":
                f"{self.attenuation.get():.3f}",
            "Launch Angle (degree)":
                f"{self.launch_angle.get():.2f}",
            "Wavelength (nm)":
                self.wavelength.get(),
            "Numerical Aperture":
                f"{NA:.5f}",
            "Critical Angle":
                f"{critical_angle:.4f}",
            "Acceptance Angle":
                f"{acceptance_angle:.4f}",
            "V-number":
                f"{v_number:.5f}",
            "Number of Modes":
                f"{number_of_modes:.2f}",
            "Output Power (mW)":
                f"{output_power:.8f}"
        }
        try:
            with open(
                CSV_FILE,
                "a",
                newline="",
                encoding="utf-8"
            ) as file:
                writer = csv.DictWriter(
                    file,
                    fieldnames=CSV_COLUMNS
                )
                writer.writerow(
                    row
                )
            self.add_row_to_table(
                row
            )
        except Exception as error:
            messagebox.showerror(
                "CSV Error",
                f"Could not save trial:\n{error}"
            )
    # ADD ROW TO TABLE
    def add_row_to_table(
        self,
        row
    ):
        values = [
            row.get(
                column,
                ""
            )
            for column in CSV_COLUMNS
        ]
        self.tree.insert(
            "",
            "end",
            values=values
        )
    # LOAD TRIALS
    def load_trials(self):
        # Clear current table
        for item in self.tree.get_children():
            self.tree.delete(
                item
            )
        if not os.path.exists(
            CSV_FILE
        ):
            return
        try:
            with open(
                CSV_FILE,
                "r",
                newline="",
                encoding="utf-8"
            ) as file:
                reader = csv.DictReader(
                    file
                )
                for row in reader:
                    self.add_row_to_table(
                        row
                    )
        except Exception as error:
            messagebox.showerror(
                "CSV Error",
                f"Could not load trial history:\n{error}"
            )
    # DELETE SELECTED TRIALS
    def delete_selected_trials(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning(
                "No Trial Selected",
                "Please select one or more trials to delete."
            )
            return
        confirm = messagebox.askyesno(
            "Delete Trial",
            f"Delete {len(selected)} selected trial(s)?"
        )
        if not confirm:
            return
        trial_numbers = []
        for item in selected:
            values = self.tree.item(
                item,
                "values"
            )
            if values:
                trial_numbers.append(
                    str(values[0])
                )
        # READ CSV
        rows = []
        try:
            with open(
                CSV_FILE,
                "r",
                newline="",
                encoding="utf-8"
            ) as file:
                reader = csv.DictReader(
                    file
                )
                for row in reader:
                    if str(
                        row["Trial No"]
                    ) not in trial_numbers:
                        rows.append(
                            row
                        )
        except Exception as error:
            messagebox.showerror(
                "CSV Error",
                f"Could not read CSV:\n{error}"
            )
            return
        # REWRITE CSV
        try:
            with open(
                CSV_FILE,
                "w",
                newline="",
                encoding="utf-8"
            ) as file:
                writer = csv.DictWriter(
                    file,
                    fieldnames=CSV_COLUMNS
                )
                writer.writeheader()
                writer.writerows(
                    rows
                )
        except Exception as error:
            messagebox.showerror(
                "CSV Error",
                f"Could not update CSV:\n{error}"
            )
            return
        # REFRESH TABLE
        self.load_trials()
        messagebox.showinfo(
            "Trial Deleted",
            "Selected trial(s) deleted successfully."
        )
    # DELETE ALL TRIALS
    def delete_all_trials(self):
        confirm = messagebox.askyesno(
            "Delete All Trials",
            "Are you sure you want to delete ALL trial data?"
        )
        if not confirm:
            return
        try:
            with open(
                CSV_FILE,
                "w",
                newline="",
                encoding="utf-8"
            ) as file:
                writer = csv.DictWriter(
                    file,
                    fieldnames=CSV_COLUMNS
                )
                writer.writeheader()
            self.load_trials()
            messagebox.showinfo(
                "Trials Deleted",
                "All trial data has been deleted."
            )
        except Exception as error:
            messagebox.showerror(
                "CSV Error",
                f"Could not delete trials:\n{error}"
            )
    # MAIN SIMULATION
    def simulate(
        self,
        save_trial=False
    ):
        n1 = self.core_index.get()
        n2 = self.cladding_index.get()
        diameter_um = (
            self.core_diameter.get()
        )
        length = (
            self.fibre_length.get()
        )
        input_power = (
            self.input_power.get()
        )
        attenuation = (
            self.attenuation.get()
        )
        launch_angle = (
            self.launch_angle.get()
        )
        wavelength_nm = (
            self.wavelength.get()
        )
        # VALIDATION
        if n1 <= n2:
            self.status_label.config(
                text="● ERROR: n₁ must be greater than n₂",
                fg=self.red
            )
            self.na_label.config(
                text="Numerical Aperture: INVALID"
            )
            self.critical_label.config(
                text="Critical Angle: INVALID"
            )
            self.acceptance_label.config(
                text="Acceptance Angle: INVALID"
            )
            self.v_number_label.config(
                text="V-number: INVALID"
            )
            self.modes_label.config(
                text="Number of Modes: INVALID"
            )
            self.output_label.config(
                text="Output Power: --"
            )
            self.loss_label.config(
                text="Total Loss: --"
            )
            self.draw_invalid_graph()
            return
        # NUMERICAL APERTURE
        NA = np.sqrt(
            n1**2 - n2**2
        )
        # CRITICAL ANGLE
        critical_angle = np.degrees(
            np.arcsin(
                n2 / n1
            )
        )
        # ACCEPTANCE ANGLE
        if NA <= 1:
            acceptance_angle = np.degrees(
                np.arcsin(
                    NA
                )
            )
        else:
            acceptance_angle = 90.0
        # V-NUMBER
        # Convert diameter from µm to metres
        diameter_m = (
            diameter_um * 1e-6
        )
        # Core radius
        radius_m = (
            diameter_m / 2
        )
        # Convert wavelength from nm to metres
        wavelength_m = (
            wavelength_nm * 1e-9
        )
        # Normalized frequency
        v_number = (
            (2 * np.pi * radius_m)
            / wavelength_m
        ) * NA
        # NUMBER OF MODES
        # Approximation for a step-index multimode fibre
        if v_number < 2.405:
            number_of_modes = 1.0
        else:
            number_of_modes = (
                v_number ** 2
            ) / 2
        # ATTENUATION LOSS
        total_loss = (
            attenuation *
            length
        )
        # OUTPUT POWER
        output_power = (
            input_power *
            10 ** (
                -total_loss / 10
            )
        )
        # UPDATE RESULTS
        self.na_label.config(
            text=f"Numerical Aperture: {NA:.4f}"
        )
        self.critical_label.config(
            text=f"Critical Angle: {critical_angle:.2f}°"
        )
        self.acceptance_label.config(
            text=f"Acceptance Angle: {acceptance_angle:.2f}°"
        )
        self.v_number_label.config(
            text=f"V-number: {v_number:.3f}"
        )
        self.modes_label.config(
            text=f"Number of Modes: {number_of_modes:.1f}"
        )
        self.output_label.config(
            text=f"Output Power: {output_power:.6f} mW"
        )
        self.loss_label.config(
            text=f"Total Loss: {total_loss:.2f} dB"
        )
        # GUIDING STATUS
        if launch_angle <= acceptance_angle:
            self.status_label.config(
                text="● LIGHT IS GUIDED",
                fg=self.green
            )
        else:
            self.status_label.config(
                text="● ANGLE EXCEEDS ACCEPTANCE",
                fg=self.orange
            )
        # LIGHT PROPAGATION GRAPH
        self.ax1.clear()
        x = np.linspace(
            0,
            length,
            1500
        )
        radius = 1.0
        number_of_rays = 9
        starting_positions = np.linspace(
            -0.8,
            0.8,
            number_of_rays
        )
        angles = np.linspace(
            -launch_angle,
            launch_angle,
            number_of_rays
        )
        # DRAW RAYS
        for y0, angle_deg in zip(
            starting_positions,
            angles
        ):
            angle_rad = np.radians(
                angle_deg
            )
            raw_y = (
                y0 +
                np.tan(angle_rad) *
                x
            )
            # Reflection-style visualization
            period = 4 * radius
            ray = (
                (
                    raw_y + radius
                )
                % period
            ) - radius
            ray = np.where(
                ray > radius,
                2 * radius - ray,
                ray
            )
            self.ax1.plot(
                x,
                ray,
                linewidth=1.5
            )
        # CORE BOUNDARIES
        self.ax1.axhline(
            radius,
            linewidth=3
        )
        self.ax1.axhline(
            -radius,
            linewidth=3
        )
        # Fibre axis
        self.ax1.axhline(
            0,
            linestyle="--",
            linewidth=1
        )
        # LABELS
        self.ax1.text(
            length * 0.02,
            1.12,
            "CORE",
            fontsize=11,
            fontweight="bold",
            color=self.blue
        )
        self.ax1.text(
            length * 0.02,
            -1.35,
            "CLADDING",
            fontsize=10,
            color=self.subtext
        )
        self.ax1.set_xlim(
            0,
            length
        )
        self.ax1.set_ylim(
            -1.5,
            1.5
        )
        self.ax1.set_xlabel(
            "Distance along fibre (km)"
        )
        self.ax1.set_ylabel(
            "Normalised position"
        )
        self.ax1.set_title(
            f"Light Propagation — "
            f"{wavelength_nm} nm",
            fontsize=13,
            fontweight="bold"
        )
        self.style_axis(
            self.ax1
        )
        # POWER GRAPH
        self.ax2.clear()
        distance = np.linspace(
            0,
            length,
            500
        )
        power = (
            input_power *
            10 ** (
                -(attenuation * distance)
                / 10
            )
        )
        self.ax2.plot(
            distance,
            power,
            linewidth=2.5
        )
        self.ax2.fill_between(
            distance,
            power,
            alpha=0.15
        )
        self.ax2.set_xlabel(
            "Distance (km)"
        )
        self.ax2.set_ylabel(
            "Optical Power (mW)"
        )
        self.ax2.set_title(
            "Optical Power vs Distance",
            fontsize=13,
            fontweight="bold"
        )
        self.style_axis(
            self.ax2
        )
        # REDRAW
        self.figure.tight_layout(
            pad=2
        )
        self.canvas.draw()
        # SAVE TRIAL
        if save_trial:
            self.save_trial(
                NA,
                critical_angle,
                acceptance_angle,
                v_number,
                number_of_modes,
                output_power
            )
    # INVALID GRAPH
    def draw_invalid_graph(self):
        self.ax1.clear()
        self.ax2.clear()
        # INVALID PARAMETERS
        self.ax1.text(
            0.5,
            0.5,
            "INVALID FIBRE PARAMETERS\n\n"
            "Core refractive index must be\n"
            "greater than cladding refractive index.",
            ha="center",
            va="center",
            transform=self.ax1.transAxes,
            fontsize=14,
            color=self.blue
        )
        self.ax2.text(
            0.5,
            0.5,
            "Simulation unavailable",
            ha="center",
            va="center",
            transform=self.ax2.transAxes,
            fontsize=14,
            color=self.blue
        )
        self.style_axis(
            self.ax1
        )
        self.style_axis(
            self.ax2
        )
        self.canvas.draw()
    # MATPLOTLIB DARK THEME
    def style_axis(
        self,
        ax
    ):
        ax.set_facecolor(
            self.panel
        )
        ax.tick_params(
            colors=self.text
        )
        ax.xaxis.label.set_color(
            self.text
        )
        ax.yaxis.label.set_color(
            self.text
        )
        ax.title.set_color(
            self.text
        )
        for spine in ax.spines.values():
            spine.set_color(
                self.subtext
            )
        ax.grid(
            True,
            alpha=0.15
        )
# START PROGRAM
if __name__ == "__main__":
    root = tk.Tk()
    app = OpticalFibreSimulator(
        root
    )
    root.mainloop()
