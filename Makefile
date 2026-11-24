# One entry point for the checks CI runs. Tool versions are pinned in
# rust-toolchain.toml, requirements-docs.txt, and the workflow files.

export CARGO_TARGET_DIR ?= $(CURDIR)/target
PYTHON ?= python3

.PHONY: check pcmkit-test oracle cpp accept harness site doctor

check: pcmkit-test oracle cpp accept harness

pcmkit-test:
	cargo fmt --all --manifest-path pcmkit/Cargo.toml --check
	cargo clippy --manifest-path pcmkit/Cargo.toml --all-targets --offline -- -D warnings
	cargo test --manifest-path pcmkit/Cargo.toml --offline --workspace

oracle: pcmkit-test
	$(PYTHON) pcmkit/oracle/test_oracle.py

cpp:
	bash pcmkit/cpp/run_consumer.sh

accept: pcmkit-test
	$(PYTHON) briefs/gain-normalize/accept.py

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
