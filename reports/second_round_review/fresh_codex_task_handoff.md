# Fresh Codex task handoff: AAPSJ second-round revision

Use this if the current Codex task cannot start local shell processes.

## User goal

Prepare the second-round AAPSJ major revision package for manuscript `AAPSJ-D-26-00263R1`.

Start by editing the local R1 manuscript package, then finalize the Response to Reviewers with exact line numbers.

## Local manuscript files

The R1 revision package is local here:

`/Users/cmontefusco/papers/python ADC predictor/Revision/`

Important files:

- `Montefusco_AAPS_linenumbered_tracked_changes.docx`
- `Abstract_linenumbered_tracked_changes.docx`
- `Keywords_tracked_changes.docx`
- `Tables_linenumbered_tracked_changes.docx`
- `Tablecaptions_linenumbered_tracked_changes.docx`
- `Figurecaptions_linenumbered_tracked_changes.docx`
- `Response_to_Reviewers.docx`
- `Supplementary_Table_S1_parameter_derivation.docx`
- `Supplementary_Table_S2_model_quality_metrics.docx`
- `Supplementary_Table_S3_comparative_tools.docx`
- `Graphical_Abstract_revised_300dpi.tif`

R1 submitted PDF to verify against:

`/Users/cmontefusco/Downloads/AAPSJ-D-26-00263_R1.pdf`

Figures:

`/Users/cmontefusco/papers/python ADC predictor/revised_figures_for_resubmission/`

## GitHub repo

Private repo:

`camontefusco/Python-based-ML-model-for-ADC-Conjugation-Platform-Selection`

Second-round branch:

`second-round-reviewer-revision-2026-08`

Draft PR:

https://github.com/camontefusco/Python-based-ML-model-for-ADC-Conjugation-Platform-Selection/pull/2

## Key second-round scaffold files in PR #2

- `reports/second_round_review/manuscript_change_map.md`
- `reports/second_round_review/manuscript_text_blocks_for_second_revision.md`
- `reports/second_round_review/Table_II_replacement.csv`
- `reports/second_round_review/Table_III_replacement.csv`
- `reports/second_round_review/predictor_variable_definitions.csv`
- `reports/second_round_review/workflow_schematic.svg`
- `reports/second_round_review/DOCX_application_checklist.md`
- `reports/second_round_review/Response_to_Reviewers_second_round_draft.md`
- `reports/second_round_review/submission_readiness_tracker.md`
- `src/feature_perturbation_sensitivity.py`

## Main scientific repositioning

The manuscript must be revised to say that the framework is a proof-of-concept post-characterization classifier / early CMC decision-support workflow.

Do **not** claim:

- validated pre-experimental platform selection;
- generalizable 1.00 model accuracy;
- that the old 19/20 threshold-rule result validates the Random Forest.

Do claim:

- internal synthetic-data audit;
- split sensitivity and uncertainty;
- literature-derived stress test / face-validity check only;
- prospective experimental or industrial validation is still required.

## Exact work order

1. Make a working copy of the R1 revision folder:
   - From `/Users/cmontefusco/papers/python ADC predictor/Revision/`
   - To `/Users/cmontefusco/papers/python ADC predictor/Revision_R2_working/`

2. Verify R1 PDF against local R1 DOCX package:
   - Check title/abstract, Table II, Table III, Figures 2/4, figure captions, supplementary tables.

3. Apply manuscript text edits:
   - Use `manuscript_text_blocks_for_second_revision.md`.
   - Mark changes according to journal instructions: boldface or highlighted text. If Word track changes are preserved, keep them too, but the current AAPSJ instruction asks for boldface/highlighted changes.

4. Replace/update tables:
   - Table II from `Table_II_replacement.csv`.
   - Table III from `Table_III_replacement.csv`.
   - Add predictor variable table from `predictor_variable_definitions.csv` either in the main manuscript or supplementary material.

5. Add workflow schematic:
   - Use `workflow_schematic.svg`; export to TIFF if needed for journal upload.
   - Add figure caption from `manuscript_text_blocks_for_second_revision.md`.

6. Rebuild line-numbered marked manuscript.

7. Add exact line numbers to:
   - `Response_to_Reviewers_second_round_draft.md`.

8. Build final response letter DOCX.

9. Final QC:
   - Abstract matches Results.
   - Table II values match repo outputs.
   - Table III no longer mixes old 19/20 rule with trained-model checks.
   - Figures/captions match panels.
   - Limitations appear in Abstract/Results/Discussion/Conclusion.
   - Response letter cites line numbers for every substantive change.

## Notes on figures

Keep R1 Figures 2 and 4 unless new analysis changes the numbers. They already address most performance/validation concerns.

Add the workflow schematic as a new figure if permitted, otherwise use it as a supplementary figure or adapt into the graphical abstract.

## Feature perturbation analysis

A script has been added:

`src/feature_perturbation_sensitivity.py`

Run it only when local Python execution is working. It outputs feature-level perturbation tables under:

`reports/feature_perturbation_sensitivity/tables/`

If not run, describe the existing noise/perturbation stress testing conservatively and do not overstate it.
