### Get Started:

```
conda create -n tppy python=3.10.13
```
```
conda activate tppy
```
```
pip3 install -r requirements.txt
```

Replace MODULE with the module under test to get the coverage:
```
pytest --cov=MODULE --cov-branch --cov-report=xml:coverage_MODULE.xml -s -q --tb=short Merged_Response/emoji/test_MODULE_merged.py
```

To get branch coverage and statement coverage:
```
python find_cumulative_coverage.py --xml coverage_MODULE.xml
```
Run the pipeline, Generate the merged test files containing all the correct unittests for the MODULE and generate the coverage report:
```
python run_pipeline.py
```