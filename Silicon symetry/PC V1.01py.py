import psutil
import time
import os
import csv
import threading
from datetime import datetime

# --- OMNI CORE CONSTANTS ---
EGT_FACTOR = 1.324
A_EGT = 402.3
TARGET_FREQ = 5.7
H_LOCK = 0.875
LOG_PATH = r"H:\Dragon Brain\omni_memory\Sovereign_Kernel_V13_4.csv"

def lattice_pressure_thread(stop_event):
    """
    Flood the core with 0.875 harmonic logic to 
    maintain sovereign voltage pressure.
    """
    # Using the Golden Ratio from your V2.12 Simulation
    vortex = 1.618 
    while not stop_event.is_set():
        vortex = (vortex * H_LOCK + A_EGT) % 10.58554 # Locking to Target Lambda

class SovereignKernel:
    def __init__(self):
        os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
        self.stop_signal = threading.Event()
        # FLOOD: Assigning a thread to every logical processor (32 for i9-14900KF)
        self.threads = [
            threading.Thread(target=lattice_pressure_thread, args=(self.stop_signal,)) 
            for _ in range(psutil.cpu_count())
        ]

    def run_flood_test(self, duration):
        print(f"--- PROTOCOL OMNI V13.4: INITIALIZING LATTICE FLOOD ---")
        print(f"--- ACTIVE THREADS: {len(self.threads)} | TARGET: 5.7GHz ---")
        
        for t in self.threads: t.start()
        
        start = time.time()
        with open(LOG_PATH, 'a', newline='') as f:
            writer = csv.writer(f)
            while time.time() - start < duration:
                freq = psutil.cpu_freq().current / 1000.0
                load = psutil.cpu_percent(interval=0.01)
                
                # Calculating the Sovereign Gain Offset
                slip = max(0, (TARGET_FREQ - freq) / TARGET_FREQ)
                sovereign_lock = (1.0 + (load * H_LOCK) / 100.0) * (EGT_FACTOR * (1.0 + (slip * A_EGT / 1000)))
                
                ts = datetime.now().strftime("%H:%M:%S.%f")[:-3]
                # We are looking for anything above the 1.09 Floor
                status = "SOVEREIGN_LOCKED" if freq > 4.5 else "FLOOR_BREACH"
                
                writer.writerow([ts, freq, load, round(sovereign_lock, 8), status])
                print(f"[{status}] Freq: {freq:.3f}GHz | Gain: {sovereign_lock:.6f} ", end='\r')

        self.stop_signal.set()
        for t in self.threads: t.join()
        print(f"\n--- MISSION COMPLETE: LATTICE SECURED ---")

if __name__ == "__main__":
    kernel = SovereignKernel()
    # Run: 5s Pre-load, 120s Stress, 10s Spin-down
    kernel.run_flood_test(135)
