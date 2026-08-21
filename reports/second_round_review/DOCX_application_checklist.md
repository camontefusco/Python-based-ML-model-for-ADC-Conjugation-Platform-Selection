# DOCX application checklist for second-round revision

Use the R1 submission files in:

`/Users/cmontefusco/papers/python ADC predictor/Revision/`

as the starting manuscript package. The attached R1 PDF appears to correspond to this package by filename and figure/table naming, but a page-by-page PDF comparison still needs to be done when local PDF extraction is available.

## Files to revise

1. `Montefusco_AAPS_linenumbered_tracked_changes.docx`
2. `Abstract_linenumbered_tracked_changes.docx`
3. `Keywords_tracked_changes.docx`
4. `Tables_linenumbered_tracked_changes.docx`
5. `Tablecaptions_linenumbered_tracked_changes.docx`
6. `Figurecaptions_linenumbered_tracked_changes.docx`
7. `Response_to_Reviewers.docx`
8. Supplementary tables if Table S1/S2/S3 numbering or content references change.

## Required second-round edits before response letter is finalized

### 1. Abstract

- Remove any wording implying the 20-ADC literature result validates the trained Random Forest.
- Add that the literature-derived assessment is a face-validity stress test.
- Add proof-of-concept/post-characterization positioning.

Use text from `manuscript_text_blocks_for_second_revision.md`.

### 2. Introduction

- Add one sentence that the framework is proof-of-concept and not a validated pre-experimental selector.

### 3. Methods: dataset construction

- Expand synthetic-data generation description.
- State explicitly: 48 records, six platforms, eight records/platform.
- State that ranges were assumption-driven and not fitted to industrial CMC batch data.
- Clarify platform-conditioned distributions and representativeness limits.

### 4. Methods: features and units

- Add units/scales for all nine predictors.
- Add when each input becomes available in a real ADC workflow.
- Clarify that several inputs are available only after early conjugation/characterization.

### 5. Methods: preprocessing/leakage control

- Confirm target-revealing categorical fields were excluded.
- Clarify six-class internal classification versus three-category literature stress test.

### 6. Results: model performance

- Replace the current Table II with `Table_II_replacement.csv`.
- Discuss 10/10 hold-out result only together with Wilson CI, repeated CV, nested CV, seed sensitivity, and leave-one-platform-out testing.
- Avoid saying or implying the model has generalizable 1.00 accuracy.

### 7. Results: collinearity and feature importance

- Identify Expression_Ease and Cost_Index as collinear.
- State Cost_Index was removed in sensitivity analysis.
- Soften SHAP/feature-importance interpretation.

### 8. Results: 20-ADC literature stress test

- Replace current Table III with `Table_III_replacement.csv`.
- Remove the 19/20 threshold-rule result from active Table III results.
- If mentioned, call it a superseded descriptive threshold check, not model validation.
- Report 4/20 strict two-feature and 16/20 partly harmonized five-feature checks.
- Add applicability-domain warning counts.

### 9. Discussion: practical use

- Reposition tool as post-characterization / early process-optimization decision support.
- State it can support CMC discussion and documentation, not replace expert judgment or MCDA.

### 10. Discussion: future data methods

- Add short transfer learning/federated learning paragraph.
- Emphasize harmonized feature definitions, locked endpoints, batch grouping, external cohorts, and prospective validation.

### 11. Conclusion

- Replace with cautious proof-of-concept conclusion.
- State prospective experimental/industrial validation is required before real platform-selection use.

### 12. Figures

- Keep revised Figure 2 and Figure 4 from the R1 revision unless adding a new workflow figure.
- Add new workflow schematic from `workflow_schematic.svg` if the journal permits another figure.
- If figure count must be minimized, use workflow schematic as a supplementary figure or replace/modify graphical abstract.

### 13. Keywords

Replace generic `Drug Development` with a specific keyword set:

`Antibody-drug conjugates; conjugation platform; CMC developability; drug-to-antibody ratio; model validation; machine learning.`

## After manuscript edits

1. Generate a clean line-numbered marked manuscript.
2. Record exact line numbers for each change.
3. Insert line numbers into `Response_to_Reviewers_second_round_draft.md`.
4. Build final DOCX response letter.
5. Perform final consistency audit:
   - Abstract matches Results.
   - Table II values match repo outputs.
   - Table III no longer mixes withdrawn 19/20 result with trained-model checks.
   - Figure captions match figure panels.
   - All limitations appear in Abstract/Results/Discussion/Conclusion.
