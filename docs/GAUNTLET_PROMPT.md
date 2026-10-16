# Gauntlet Loop

Build RoomPlan to USER_REQUIREMENTS.md including the latest user clarifications. Compare real exports with the applicable Floorplanner bar in quality-bar.md: attractive listing plans and clear ordinary Three.js scenes and walkthroughs. Ray tracing and photorealism are excluded; a separate generative module will provide photorealism later.

Choose the approach. Divide the goal into the smallest independently improvable and judgeable pieces. For each important piece, use a builder and a separate critic with fresh context. Critics must inspect real output, compare directly with the bar, use blind A/B where practical, and send the biggest remaining gap back for another round. Keep looping until the output wins or the user stops. Maintain a simple live progress page with actual artifacts, failures and next gaps. Use subagents; do not impose a fixed round count.

User clarification: object reconstruction will use a local GPU service connected later. Its adapter, source retention and honest unavailable state remain in scope; actual GPU inference is deferred.
