!(import! &self /home/brian/PeTTa/repos/Omega/src/utils)
!(import! &self /home/brian/PeTTa/repos/Omega/src/logger.py)
!(import! &self /home/brian/PeTTa/repos/Omega/src/log)
!(import! &self /home/brian/PeTTa/repos/Omega/src/plugin)

!(initLogger)

!(loadPlugin (metta "truthbridge" "/home/brian/TruthBridge/omega_plugin"))

!(truthbridge-resolve contradict strong weak)
