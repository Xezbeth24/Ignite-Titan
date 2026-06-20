#!/usr/bin/env python3
"""Benchmark audit performance: fast mode vs full mode."""
import sys
import time
from src.auditor import audit_protocol

# Sample protocol text (short for quick testing)
sample_protocol = """
Clinical Protocol: Study of Drug Safety in Patients with Hypertension

Objective: To evaluate the safety profile of Compound X in hypertensive patients.

Methods:
- Patient population: 100 adults aged 40-75 with moderate hypertension
- Duration: 12 weeks
- Dosage: 50mg daily
- Safety monitoring: Weekly blood pressure checks, monthly labs

Inclusion criteria:
- Age 40-75
- Systolic BP 140-180 mmHg
- No prior adverse reactions

Exclusion criteria:
- Pregnancy
- Severe kidney disease
- Concurrent beta-blocker use

Expected outcomes:
- 20% reduction in systolic BP without adverse events
- Safety profile comparable to standard antihypertensives
"""

print("=" * 60)
print("AUDIT PERFORMANCE BENCHMARK")
print("=" * 60)

# Fast mode
print("\n[FAST MODE] Running audit with guidelines-only retrieval...")
start_fast = time.time()
try:
    result_fast = audit_protocol(sample_protocol, fast_mode=True)
    time_fast = time.time() - start_fast
    print(f"Fast mode result:\n{result_fast[:200]}...\n")
    print(f"✓ Fast mode completed in {time_fast:.1f}s")
except Exception as e:
    print(f"✗ Fast mode failed: {e}")
    time_fast = None

# Full mode (only if Gemini API is available)
print("\n[FULL MODE] Running audit with Gemini LLM analysis...")
import os
if os.getenv("GEMINI_API_KEY"):
    start_full = time.time()
    try:
        result_full = audit_protocol(sample_protocol, fast_mode=False)
        time_full = time.time() - start_full
        print(f"Full mode result:\n{result_full[:200]}...\n")
        print(f"✓ Full mode completed in {time_full:.1f}s")
    except Exception as e:
        print(f"✗ Full mode failed: {e}")
        time_full = None
else:
    print("⚠ GEMINI_API_KEY not set; skipping full mode")
    time_full = None

# Summary
print("\n" + "=" * 60)
print("SUMMARY")
print("=" * 60)
if time_fast:
    print(f"Fast mode (guidelines only): {time_fast:.1f}s")
if time_full:
    print(f"Full mode (with LLM):        {time_full:.1f}s")
    if time_fast:
        speedup = time_full / time_fast
        print(f"\nSpeedup factor: {speedup:.1f}x faster with fast mode")
else:
    if time_fast:
        print(f"\nFast mode is ready to use. To enable full mode, set GEMINI_API_KEY.")
