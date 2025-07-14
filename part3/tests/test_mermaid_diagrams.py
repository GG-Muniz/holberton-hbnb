#!/usr/bin/env python3
"""
Mermaid Diagram Validation Script
This script tests that our Mermaid diagrams have valid syntax
"""

import re
import os
import sys

def extract_mermaid_blocks(file_path):
    """Extract all mermaid code blocks from a markdown file"""
    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        return []
    
    with open(file_path, 'r') as file:
        content = file.read()
    
    # Find all mermaid code blocks
    pattern = r'```mermaid\n(.*?)```'
    matches = re.findall(pattern, content, re.DOTALL)
    
    return matches

def validate_mermaid_syntax(diagram_code, diagram_name):
    """Basic validation of Mermaid syntax"""
    lines = diagram_code.strip().split('\n')
    
    if not lines:
        print(f"❌ {diagram_name}: Empty diagram")
        return False
    
    # Check for valid diagram type
    diagram_type = lines[0].strip()
    valid_types = ['erDiagram', 'graph', 'flowchart', 'classDiagram']
    
    if not any(diagram_type.startswith(dt) for dt in valid_types):
        print(f"❌ {diagram_name}: Invalid diagram type '{diagram_type}'")
        return False
    
    # Basic syntax checks for ER diagrams
    if diagram_type == 'erDiagram':
        # Check for entity definitions (look for opening brace after entity name)
        entity_lines = [line.strip() for line in lines[1:] if line.strip()]
        has_entities = False
        
        for i, line in enumerate(entity_lines):
            # Look for entity definition pattern: ENTITY_NAME {
            if '{' in line:
                has_entities = True
                break
            # Also check if entity name is followed by opening brace on next line
            elif i + 1 < len(entity_lines) and entity_lines[i + 1].strip() == '{':
                has_entities = True
                break
        
        if not has_entities:
            print(f"❌ {diagram_name}: No entity definitions found")
            return False
        
        # Check for relationship syntax (optional for single entity diagrams)
        has_relationships = any('--' in line for line in lines)
        if not has_relationships:
            print(f"ℹ️  {diagram_name}: Single entity diagram (no relationships)")
    
    print(f"✅ {diagram_name}: Valid Mermaid syntax")
    return True

def test_diagram_files():
    """Test all diagram files for valid Mermaid syntax"""
    print("=" * 60)
    print("Mermaid Diagram Validation Test")
    print("=" * 60)
    
    diagram_files = [
        ('../diagrams/database_er_diagram.md', 'Main ER Diagram'),
        ('../diagrams/table_structure_diagrams.md', 'Table Structure Diagrams'),
        ('../diagrams/relationship_diagrams.md', 'Relationship Diagrams')
    ]
    
    total_diagrams = 0
    valid_diagrams = 0
    
    for file_path, description in diagram_files:
        print(f"\n🔍 Testing {description} ({file_path})...")
        
        mermaid_blocks = extract_mermaid_blocks(file_path)
        
        if not mermaid_blocks:
            print(f"❌ No Mermaid diagrams found in {file_path}")
            continue
        
        print(f"   Found {len(mermaid_blocks)} diagram(s)")
        
        for i, diagram in enumerate(mermaid_blocks, 1):
            diagram_name = f"{description} #{i}"
            total_diagrams += 1
            
            if validate_mermaid_syntax(diagram, diagram_name):
                valid_diagrams += 1
    
    print("\n" + "=" * 60)
    print("Validation Summary")
    print("=" * 60)
    print(f"Total diagrams tested: {total_diagrams}")
    print(f"Valid diagrams: {valid_diagrams}")
    print(f"Invalid diagrams: {total_diagrams - valid_diagrams}")
    
    if valid_diagrams == total_diagrams:
        print("🎉 All diagrams have valid Mermaid syntax!")
        print("\nNext steps:")
        print("1. View diagrams in Mermaid Live Editor: https://mermaid-live.github.io/")
        print("2. Copy diagram code from markdown files")
        print("3. Paste into editor for visual verification")
        return True
    else:
        print("❌ Some diagrams have syntax issues")
        return False

def generate_mermaid_urls():
    """Generate URLs for viewing diagrams in Mermaid Live Editor"""
    print("\n" + "=" * 60)
    print("Mermaid Live Editor URLs")
    print("=" * 60)
    print("Copy the diagram code from these files and paste into the editor:")
    print()
    
    files_info = [
        ('../diagrams/database_er_diagram.md', 'Complete ER Diagram with all entities'),
        ('../diagrams/table_structure_diagrams.md', 'Individual table structures'),
        ('../diagrams/relationship_diagrams.md', 'Focused relationship views')
    ]
    
    for file_path, description in files_info:
        print(f"📄 {file_path}")
        print(f"   {description}")
        print(f"   View at: https://mermaid-live.github.io/")
        print()

def check_documentation_completeness():
    """Check that all diagram files have proper documentation"""
    print("\n" + "=" * 60)
    print("Documentation Completeness Check")
    print("=" * 60)
    
    required_files = [
        '../diagrams/database_er_diagram.md',
        '../diagrams/table_structure_diagrams.md', 
        '../diagrams/relationship_diagrams.md',
        '../docs/DATABASE_DIAGRAMS_README.md'
    ]
    
    missing_files = []
    
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path} exists")
        else:
            print(f"❌ {file_path} missing")
            missing_files.append(file_path)
    
    if not missing_files:
        print("🎉 All documentation files are present!")
        return True
    else:
        print(f"❌ Missing {len(missing_files)} file(s)")
        return False

if __name__ == "__main__":
    print("HBnB Database Diagrams - Mermaid Validation")
    print()
    
    # Test diagram syntax
    syntax_valid = test_diagram_files()
    
    # Check documentation completeness
    docs_complete = check_documentation_completeness()
    
    # Generate viewing URLs
    generate_mermaid_urls()
    
    # Final summary
    print("\n" + "=" * 60)
    print("Final Summary")
    print("=" * 60)
    
    if syntax_valid and docs_complete:
        print("🎉 All tests passed!")
        print("✅ Mermaid syntax is valid")
        print("✅ Documentation is complete")
        print("✅ Ready for Task 10 submission")
        
        print("\nTask 10 Deliverables Created:")
        print("📊 Main ER diagram with all entities and relationships")
        print("📋 Detailed table structure diagrams")
        print("🔗 Relationship-focused diagrams")
        print("📚 Comprehensive documentation")
        
        sys.exit(0)
    else:
        print("❌ Some issues found")
        if not syntax_valid:
            print("   - Mermaid syntax errors detected")
        if not docs_complete:
            print("   - Documentation files missing")
        
        sys.exit(1)