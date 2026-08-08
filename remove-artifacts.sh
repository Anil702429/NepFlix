#!/bin/bash
# Script to remove tracked development artifacts from NepFlix repository
# Run this from the repository root: bash remove-artifacts.sh

set -e  # Exit on error

echo "=== Removing Development Artifacts from Git Tracking ==="
echo ""

# Remove db.sqlite3 from Git tracking
echo "1. Removing db.sqlite3..."
git rm --cached db.sqlite3
echo "   ✓ db.sqlite3 removed from Git (local file preserved)"

# Remove all __pycache__ directories
echo ""
echo "2. Removing __pycache__ directories..."
find . -type d -name __pycache__ -exec git rm -r --cached {} + 2>/dev/null || true
echo "   ✓ All __pycache__ directories removed from Git"

# Remove all .pyc files
echo ""
echo "3. Removing .pyc files..."
find . -type f -name "*.pyc" -exec git rm --cached {} + 2>/dev/null || true
echo "   ✓ All .pyc files removed from Git"

# Remove all .pyo files
echo ""
echo "4. Removing .pyo files..."
find . -type f -name "*.pyo" -exec git rm --cached {} + 2>/dev/null || true
echo "   ✓ All .pyo files removed from Git"

# Create the commit
echo ""
echo "5. Creating commit..."
git commit -m "Remove development artifacts from tracking (db.sqlite3, __pycache__, *.pyc, *.pyo)" \
    || echo "   (No changes to commit - artifacts may already be removed)"

echo ""
echo "=== Removal Complete ==="
echo ""
echo "Status Report:"
git status

echo ""
echo "Artifacts removed from tracking:"
git log -1 --name-status

echo ""
echo "Next steps:"
echo "  1. Run: python manage.py check"
echo "  2. Verify migrations are intact: git log --name-only | grep migrations"
echo "  3. Push to GitHub: git push origin main"
