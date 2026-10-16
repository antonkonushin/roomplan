# Gauntlet Loop

Build RoomPlan to the full specification in USER_REQUIREMENTS.md. Match and then beat the frozen Floorplanner listing-plan, dollhouse and interior references in quality-bar.md with real exports from the working app.

Choose the approach. Divide the goal into the smallest independently improvable and judgeable pieces. For each important piece, use a builder and a separate critic with fresh context. Critics must inspect real output, compare directly with the bar, use blind A/B where practical, and send the biggest remaining gap back for another round. Keep looping until the output wins or the user stops. Maintain a simple live progress page with actual artifacts, failures and next gaps. Use subagents; do not impose a fixed round count.

User clarification: object reconstruction will use a local GPU service connected later. Its adapter, source retention and honest unavailable state remain in scope; actual GPU inference is deferred.
