; TruthBridge + Omega integration test

!(import! &self /home/brian/PeTTa/repos/Omega/src/utils)
!(import! &self /home/brian/PeTTa/repos/Omega/src/logger.py)
!(import! &self /home/brian/PeTTa/repos/Omega/src/log)
!(import! &self /home/brian/PeTTa/repos/Omega/src/plugin)

!(initLogger)

; Load the TruthBridge Omega plugin
!(loadPlugin
    (metta "truthbridge"
        "/home/brian/TruthBridge/omega_plugin"))

; Test the TruthBridge MeTTa skill directly
!(truthbridge-resolve
    contradict
    strong
    weak)
