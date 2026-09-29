; =========================================================
; TruthBridge Omega Plugin
; =========================================================
;
; This plugin exposes the TruthBridge symbolic resolution
; function to the Omega agent.
;
; Inputs:
;   relationship
;   evidence strength for Agent A
;   evidence strength for Agent B
;
; Supported relationships:
;   agree
;   qualify
;   contradict
;   unrelated
;
; Evidence strength:
;   strong
;   moderate
;   weak
;   none
;
; =========================================================


; ---------------------------------------------------------
; OMEGA PLUGIN ENTRY POINT
; ---------------------------------------------------------

(= (loadOmegaPlugin)
   (progn
     (add-skill
       truthbridge-resolve
       "Resolve two competing TruthBridge claims using their logical relationship and evidence strength."
       (relationship evidence_a evidence_b))
     ()
   ))


; ---------------------------------------------------------
; AGREEMENT
; ---------------------------------------------------------

(= (truthbridge-resolution agree $a $b)
   (truthbridge-result
     agreement
     "The two agents substantially agree, so no conflict resolution is required."))


; ---------------------------------------------------------
; QUALIFICATION
; ---------------------------------------------------------

(= (truthbridge-resolution qualify $a $b)
   (truthbridge-result
     qualified-resolution
     "One claim qualifies, limits, or adds conditions to the other. TruthBridge preserves the qualification instead of forcing a binary winner."))


; ---------------------------------------------------------
; UNRELATED CLAIMS
; ---------------------------------------------------------

(= (truthbridge-resolution unrelated $a $b)
   (truthbridge-result
     unrelated-claims
     "The claims do not address the same proposition, so their evidence is not treated as competing evidence."))


; ---------------------------------------------------------
; CONTRADICTION: INSUFFICIENT EVIDENCE
; ---------------------------------------------------------

(= (truthbridge-resolution contradict none none)
   (truthbridge-result
     insufficient-evidence
     "The claims contradict each other, but neither claim has supporting evidence."))


; ---------------------------------------------------------
; CONTRADICTION: AGENT A BETTER SUPPORTED
; ---------------------------------------------------------

(= (truthbridge-resolution contradict strong weak)
   (truthbridge-result
     claim-a-better-supported
     "The claims contradict each other and Agent A has stronger supporting evidence."))

(= (truthbridge-resolution contradict strong none)
   (truthbridge-result
     claim-a-better-supported
     "The claims contradict each other and Agent A has strong supporting evidence while Agent B has none."))

(= (truthbridge-resolution contradict moderate weak)
   (truthbridge-result
     claim-a-better-supported
     "The claims contradict each other and Agent A has stronger supporting evidence."))

(= (truthbridge-resolution contradict moderate none)
   (truthbridge-result
     claim-a-better-supported
     "The claims contradict each other and Agent A has moderate supporting evidence while Agent B has none."))

(= (truthbridge-resolution contradict strong moderate)
   (truthbridge-result
     claim-a-better-supported
     "The claims contradict each other and Agent A has stronger supporting evidence."))


; ---------------------------------------------------------
; CONTRADICTION: AGENT B BETTER SUPPORTED
; ---------------------------------------------------------

(= (truthbridge-resolution contradict weak strong)
   (truthbridge-result
     claim-b-better-supported
     "The claims contradict each other and Agent B has stronger supporting evidence."))

(= (truthbridge-resolution contradict none strong)
   (truthbridge-result
     claim-b-better-supported
     "The claims contradict each other and Agent B has strong supporting evidence while Agent A has none."))

(= (truthbridge-resolution contradict weak moderate)
   (truthbridge-result
     claim-b-better-supported
     "The claims contradict each other and Agent B has stronger supporting evidence."))

(= (truthbridge-resolution contradict none moderate)
   (truthbridge-result
     claim-b-better-supported
     "The claims contradict each other and Agent B has moderate supporting evidence while Agent A has none."))

(= (truthbridge-resolution contradict moderate strong)
   (truthbridge-result
     claim-b-better-supported
     "The claims contradict each other and Agent B has stronger supporting evidence."))


; ---------------------------------------------------------
; CONTRADICTION: EVIDENCE TOO CLOSE
; ---------------------------------------------------------

(= (truthbridge-resolution contradict strong strong)
   (truthbridge-result
     unresolved
     "Both contradictory claims have strong supporting evidence, so MeTTa does not select a winner."))

(= (truthbridge-resolution contradict moderate moderate)
   (truthbridge-result
     unresolved
     "Both contradictory claims have comparable moderate evidence, so MeTTa does not select a winner."))

(= (truthbridge-resolution contradict weak weak)
   (truthbridge-result
     unresolved
     "Both contradictory claims have comparable weak evidence, so MeTTa does not select a winner."))


; ---------------------------------------------------------
; DEFAULT CONTRADICTION CASES
; ---------------------------------------------------------

(= (truthbridge-resolution contradict weak none)
   (truthbridge-result
     claim-a-better-supported
     "The claims contradict each other and Agent A has supporting evidence while Agent B has none."))

(= (truthbridge-resolution contradict none weak)
   (truthbridge-result
     claim-b-better-supported
     "The claims contradict each other and Agent B has supporting evidence while Agent A has none."))


; ---------------------------------------------------------
; PUBLIC TRUTHBRIDGE SKILL
; ---------------------------------------------------------

(= (truthbridge-resolve $relationship $evidence_a $evidence_b)
   (truthbridge-resolution
     $relationship
     $evidence_a
     $evidence_b))
