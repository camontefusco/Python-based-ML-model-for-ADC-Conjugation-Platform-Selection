# Second-round submission readiness tracker

Last updated: 2026-08-21

## Current status

The second-round scientific revision plan is prepared in this branch. The R1 manuscript package appears to be available locally in:

`/Users/cmontefusco/papers/python ADC predictor/Revision/`

The GitHub repository is private and contains the recovered project source, datasets, notebooks, scripts, outputs, and second-round revision scaffold.

## Done in GitHub branch

- [x] Created second-round branch: `second-round-reviewer-revision-2026-08`
- [x] Opened draft PR #2
- [x] Added reviewer-to-manuscript change map
- [x] Added replacement Table II structure
- [x] Added replacement Table III structure
- [x] Added predictor-variable definitions with units and practical meaning
- [x] Added plain-language manuscript text blocks
- [x] Added second-round response letter draft
- [x] Added workflow schematic specification
- [x] Added editable workflow schematic SVG
- [x] Added DOCX application checklist
- [x] Added feature perturbation sensitivity script

## Not yet done

These steps require local DOCX/PDF access or a working local execution environment.

- [ ] Verify `AAPSJ-D-26-00263_R1.pdf` page-by-page against the R1 DOCX package.
- [ ] Apply second-round text changes to `Montefusco_AAPS_linenumbered_tracked_changes.docx`.
- [ ] Apply Abstract changes to `Abstract_linenumbered_tracked_changes.docx`.
- [ ] Update `Keywords_tracked_changes.docx`.
- [ ] Replace/modify Tables II and III in `Tables_linenumbered_tracked_changes.docx`.
- [ ] Update table captions.
- [ ] Add or place the new workflow schematic as a manuscript figure or supplementary figure.
- [ ] Update figure captions.
- [ ] Generate a fresh line-numbered marked manuscript.
- [ ] Insert exact manuscript line numbers into the response letter.
- [ ] Build final DOCX response letter.
- [ ] Run final consistency review across Abstract, Results, Tables, Figures, Discussion, Conclusion, and Response letter.

## Recommended order once DOCX editing is available

1. Copy the R1 local revision folder to a new folder named `Revision_R2_working`.
2. Apply the manuscript text blocks from `manuscript_text_blocks_for_second_revision.md`.
3. Replace Table II using `Table_II_replacement.csv`.
4. Replace Table III using `Table_III_replacement.csv`.
5. Add predictor-variable definition table either as a main table or supplementary table.
6. Add workflow schematic from `workflow_schematic.svg` or convert it to journal-acceptable TIFF.
7. Update captions.
8. Rebuild the line-numbered version.
9. Add line numbers to `Response_to_Reviewers_second_round_draft.md`.
10. Export final DOCX/PDF package for review.

## Scientific choices to preserve

- Do not defend the original 1.00 hold-out accuracy as generalizable performance.
- Do not present the old 19/20 threshold-rule result as external validation.
- Do not claim the model is a validated pre-experimental platform-selection tool.
- Do position the work as a proof-of-concept post-characterization classifier and early CMC decision-support workflow.
- Do emphasize that prospective experimental or industrial validation remains required.

## Figure handling

Keep R1 Figure 2 and Figure 4 unless new analysis changes the underlying numbers. These figures already address many reviewer concerns:

- Figure 2: repeated CV, seed sensitivity, leave-one-platform-out transfer, redundant-feature sensitivity.
- Figure 4: strict and partly harmonized literature stress tests, DAR space, applicability-domain warnings.

Add the workflow schematic only if the journal allows another figure. If figure count is constrained, use it as a supplementary figure or adapt it into the graphical abstract.

## Response letter handling

The response letter draft is intentionally not final because it lacks exact line numbers. The final response letter should be generated only after the line-numbered marked manuscript is rebuilt.
