# One entry point for the checks CI runs. Tool versions are pinned in
# rust-toolchain.toml, requirements-docs.txt, and the workflow files.

export CARGO_TARGET_DIR ?= $(CURDIR)/target
PYTHON ?= python3

.PHONY: check fast pcmkit-test flaky python-lint tidy cpp oracle mutation e2e accept sanitizers harness site doctor

check: fast oracle mutation e2e accept sanitizers harness

fast: pcmkit-test flaky python-lint tidy cpp

pcmkit-test:
	cargo fmt --all --manifest-path pcmkit/Cargo.toml --check
	cargo clippy --manifest-path pcmkit/Cargo.toml --all-targets --offline -- -D warnings
	cargo test --manifest-path pcmkit/Cargo.toml --offline --workspace

flaky:
	$(PYTHON) pcmkit/fast/flaky_scan.py pcmkit briefs

python-lint:
	bash pcmkit/fast/python_lint.sh

tidy:
	bash pcmkit/cpp/run_tidy.sh

cpp:
	bash pcmkit/cpp/run_consumer.sh

oracle: pcmkit-test
	$(PYTHON) pcmkit/oracle/test_oracle.py

mutation:
	$(PYTHON) pcmkit/oracle/mutation_smoke.py

e2e: pcmkit-test
	$(PYTHON) pcmkit/e2e/prove.py

accept: pcmkit-test
	$(PYTHON) briefs/gain-normalize/accept.py

sanitizers:
	bash pcmkit/cpp/run_sanitizers.sh

harness:
	$(PYTHON) -m unittest discover -s tests -v

site:
	$(PYTHON) -m zensical build --strict --clean

doctor:
	@$(PYTHON) --version
	@rustc --version
	@cargo --version
	@g++ --version | head -n 1
	@df -h . | awk 'NR==1 || NR==2'
	@du -sh target site .venv 2>/dev/null || true
