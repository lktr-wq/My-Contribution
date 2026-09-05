# Capture limitations

- Local date 2026-09-06 (Asia/Shanghai); UTC timestamps fall on 2026-09-05.
- Initial snapshot script saved search-0 through search-3 successfully: 33, 61, 1, 15 results. All four have incomplete_results=false and item count equals total_count. Deduplicated index: 100 issues/PRs.
- The subsequent GET https://api.github.com/repos/NVIDIA/cccl/pulls/9762 failed with API rate limit exceeded. No PR-detail responses, issue comments, or API main-commit response were captured. The initial script only wrote the request manifest at completion, so that manifest is absent. Script error handling was improved afterwards; do not interpret that improvement as a second successful run.
- Read-only `git ls-remote https://github.com/NVIDIA/cccl.git refs/heads/main` succeeded and returned `486de1c44daf7d1a343cbbf0f5477e9bea8ad600 refs/heads/main`. No fetch, checkout, or upstream write was performed.
- Three source files were requested at that immutable commit. The first agent_reduce.cuh request failed TLS establishment; a single retry succeeded. Both the failed request and successful retry are recorded separately. TLS verification was not disabled.
- Search indexes include bodies but not all review threads, diffs, or comments. This is a bounded relevance check, not an exhaustive novelty guarantee.
