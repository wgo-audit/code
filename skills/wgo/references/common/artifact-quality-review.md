# Artifact Quality Review

Run once after a detailed reviewer drafts its selected outputs and before it
writes its report. This is an ephemeral review, not an audit artifact, gate,
or second workflow. A bounded quality worker reads only the draft outputs, the
reviewer question, and their cited evidence; it returns concrete edits and does
not write files or shared audit state.

Check whether each artifact:

1. helps the stated reader make a decision or safely act;
2. makes each material relationship, boundary, or state clear rather than
   merely restating prose;
3. separates confirmed evidence, inference, and unknowns; and
4. would be clearer if split, replaced, or expressed as a diagram, table, or
   short narrative; and
5. supports zero or more decision insights only where the evidence changes a
   decision, priority, sequence, claim, or stop condition.
6. identifies evidence-supported strengths that reduce a stated mandate concern,
   when any exist, without treating an evidence gap as a strength.

A decision-insight candidate must state the decision, causal relationship or
conflict, consequence, and smallest next proof/action. Reject fact restatements,
generic risks, and invented recommendations. Do not require or cap candidates.

For a diagram, reject decorative box-and-arrow prose: it must clarify a
relationship the reader needs to reason about. For a table or narrative, reject
it when a diagram would more clearly show a material flow, dependency,
handoff, boundary, or state transition. The reviewer revises once from the
feedback; do not create a review record.

For a horizontal flow, reject a bare left-to-right chain or a layout that relies
on viewport shrinking. Require compact left-to-right stages in a top-to-bottom
graph with boundary connections, or a plain top-to-bottom graph when exact
cross-stage node links are material.
