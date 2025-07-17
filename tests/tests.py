import os
import sys

def assert_exists(path, name):
    """
    Asserts that a given file or directory path exists.
    Raises an AssertionError if the path does not exist.
    """
    if not os.path.exists(path):
        raise AssertionError(f"Missing: {name} at {path}")
    print(f"✅ Found {name} at {path}")

def validate_pbip_structure(pbip_base_dir):
    """
    Validates the expected file structure of a Power BI Project (.pbip).
    """
    # Ensure the base directory exists
    assert_exists(pbip_base_dir, "Power BI project base directory")

    # Find the .pbip file to determine the project name
    pbip_files = [f for f in os.listdir(pbip_base_dir) if f.lower().endswith('.pbip')]
    if not pbip_files:
        raise AssertionError(f"No .pbip file found in {pbip_base_dir}")
    if len(pbip_files) > 1:
        print(f"⚠️ Warning: Multiple .pbip files found in {pbip_base_dir}. Using the first one: {pbip_files[0]}")
    
    pbip_file_name = pbip_files[0]
    # Extracting project name, e.g., "AdventureWorks Report" from "AdventureWorks Report.pbip"
    project_name = os.path.splitext(pbip_file_name)[0] # This handles cases like 'AdventureWorks Report Main.pbix' as well, using the base name before extension

    print(f"🔍 Validating PBIP structure for project: '{project_name}'...")

    # Validate the main .pbip file
    pbip_file_path = os.path.join(pbip_base_dir, pbip_file_name)
    assert_exists(pbip_file_path, ".pbip file")

    # Validate the Report JSON file
    # Based on your ls -RF output: powerbi/AdventureWorks Report.Report/definition/report.json
    report_json_folder_name = f"{project_name}.Report"
    report_json_dir = os.path.join(pbip_base_dir, report_json_folder_name, "definition")
    report_json_file = os.path.join(report_json_dir, "report.json")
    assert_exists(report_json_file, "Report JSON file")

    # Validate the Semantic Model (TMDL) file
    # Based on your ls -RF output: powerbi/AdventureWorks Report.SemanticModel/definition/model.tmdl
    semantic_model_folder_name = f"{project_name}.SemanticModel" # Corrected casing and removed space
    model_dir = os.path.join(pbip_base_dir, semantic_model_folder_name)
    model_file = os.path.join(model_dir, "definition", "model.tmdl") # Included 'definition' subfolder
    assert_exists(model_file, "Semantic Model file (TMDL)")

    print("✅ PBIP structure validation complete!")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python tests/tests.py <path_to_pbip_directory>")
        sys.exit(1)
    
    # The script expects the path to the directory containing the .pbip file,
    # e.g., 'powerbi/'
    pbip_directory_to_test = sys.argv[1]
    validate_pbip_structure(pbip_directory_to_test)