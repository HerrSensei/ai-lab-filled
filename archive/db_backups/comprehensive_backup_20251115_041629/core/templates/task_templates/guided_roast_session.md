# Task Template: Guided Roast Session

## 🎯 Task Overview

**Task Type:** Code Review & Architecture Analysis
**Target Audience:** Junior Software Engineer
**Style:** Sassy Expert Roast mit konstruktiven Lösungen
**Duration:** 30-45 Minuten
**Output:** Verbesserte Projektstruktur + Dokumentation

---

## 📋 Task Specification

### Primary Objective
Führe eine schonungslose Analyse einer Projektstruktur durch, identifiziere Probleme und löse sie Schritt für Schritt mit dem User interaktiv.

### Success Criteria
- [ ] Projektstruktur analysiert und bewertet
- [ ] Probleme identifiziert und priorisiert
- [ ] Lösungen schrittweise implementiert
- [ ] User hat Verständnis für die Änderungen
- [ ] Ergebnisse dokumentiert

---

## 🔄 Execution Workflow

### Phase 1: Initial Analysis (5-10 min)

#### 1.1 Structure Discovery
```bash
# Discover project structure
list /path/to/project --recursive

# Look for common anti-patterns
glob "**/.DS_Store"
glob "**/README.md"
glob "**/*.template"
```

#### 1.2 Pattern Recognition
Check for:
- [ ] Duplicate files/templates
- [ ] Misplaced directories (projects at end?)
- [ ] OS-specific files (.DS_Store, Thumbs.db)
- [ ] README overdocumentation
- [ ] Inconsistent naming
- [ ] Empty directories

#### 1.3 Generate Initial Roast
Create 3 roast versions:
1. **Standard Roast** (`roast.md`) - Professional but firm
2. **Sassy Roast** (`roast_by_opencode.md`) - Sarcastic but constructive
3. **Gottlose Roast** (`roast_gottlos.md`) - Brutally honest with update

### Phase 2: Interactive Problem Solving (20-30 min)

#### 2.1 Point-by-Point Review
For each identified problem:

1. **Present Problem:** "Das Problem ist X..."
2. **Explain Impact:** "Warum das scheiße ist..."
3. **Propose Solution:** "Mein Fix-Vorschlag..."
4. **Get Confirmation:** "Bestätigst du das oder lehnst du ab?"

#### 2.2 Implementation Pattern
```bash
# For file operations
if confirmed:
    execute_fix()
    verify_result()
else:
    discuss_alternative()
```

#### 2.3 Common Fix Patterns

**Template Consolidation:**
```bash
mkdir -p templates/
cp -r source1/templates/* templates/
cp -r source2/templates/* templates/
rm -rf source1/templates/ source2/templates/
```

**Documentation Organization:**
```bash
mkdir -p docs/
mv scattered_readmes/* docs/
rename_files_to_meaningful_names()
```

**OS File Cleanup:**
```bash
find . -name ".DS_Store" -delete
echo "**/.DS_Store" >> .gitignore
```

### Phase 3: Documentation & Follow-up (5-10 min)

#### 3.1 Create Change Log
```markdown
# AI Lab Change Log

## YYYY-MM-DD - [Change Description]

### Änderungen
- [What was done]

### Betroffene Dateien
```
✅ ADDED:
- new_files

🔄 MODIFIED:
- changed_files

❌ DELETED:
- removed_files
```

### Rollback Commands
```bash
# Rollback commands here
```
```

#### 3.2 Generate Task Summary
Create final documentation including:
- Problems identified vs solved
- Before/after comparison
- Lessons learned
- Next steps recommendations

#### 3.3 Roast Consolidation & Humorful Processing
Create a consolidated roast summary that combines all three roast styles:

```markdown
# 🎭 THE GREAT ROAST CONSOLIDATION - [Project Name]

## 📊 Roast Statistics

| Roast Style | Problems Found | Problems Solved | Roast Intensity |
|-------------|---------------|-----------------|-----------------|
| Professional | X | Y | 🌶️ Mild |
| Sassy | X | Y | 🌶️🌶️ Medium |
| Gottlose | X | Y | 🌶️🌶️🌶️ Brutal |

**Total Problems Identified:** X
**Total Problems Solved:** Y
**Success Rate:** Z%

---

## 🔥 The Greatest Hits Collection

### Most Brutal Burn
> [Select the most savage quote from all three roasts]

### Most Accurate Analogy
> [Select the analogy that hit closest to home]

### Most Constructive Roast
> [Select the roast that led to the best improvement]

---

## 🎭 Roast Style Analysis

### Professional Roast - "The Corporate Consultant"
**Strengths:**
- Industry best practices
- Actionable recommendations
- Professional tone

**Weaknesses:**
- Too polite for real impact
- Sometimes boring AF

**Best Quote:**
> [Select best professional roast]

---

### Sassy Roast - "The Sarcastic Senior Dev"
**Strengths:**
- Hilarious analogies
- Memorable comparisons
- Still technically accurate

**Weaknesses:**
- Sometimes too much sass
- Might hurt feelings (who cares?)

**Best Quote:**
> [Select best sassy roast]

---

### Gottlose Roast - "The No-Filter Truth Bomb"
**Strengths:**
- Brutal honesty
- No sugar-coating
- Raw technical feedback

**Weaknesses:**
- Might cause existential crisis
- Requires therapy afterwards

**Best Quote:**
> [Select best gottlose roast]

---

## 🏆 The Roast Awards Ceremony

### 🥇 "Most Likely to Make You Cry" Award
Goes to: [Most brutal roast line]

### 🥈 "Most Technically Accurate" Award
Goes to: [Most correct technical criticism]

### 🥉 "Funniest But Still Helpful" Award
Goes to: [Most humorous but useful roast]

### 🏅 "Biggest Glow Up" Award
Goes to: [Most dramatic improvement made]

---

## 📈 Before vs After: The Glow Up

### Before Roast
```
🏚️ Project Structure: [Rating]/10
📚 Documentation: [Rating]/10
🔧 Code Quality: [Rating]/10
🚀 Deployment: [Rating]/10
💡 Overall Vibe: [Rating]/10
```

### After Roast
```
✨ Project Structure: [Rating]/10 (+X)
📚 Documentation: [Rating]/10 (+X)
🔧 Code Quality: [Rating]/10 (+X)
🚀 Deployment: [Rating]/10 (+X)
💡 Overall Vibe: [Rating]/10 (+X)
```

**Total Improvement:** +X points! 🎉

---

## 🎯 Lessons Learned (The Hard Way)

### What We Discovered About Your Project
1. **[Lesson 1]** - [Brief explanation]
2. **[Lesson 2]** - [Brief explanation]
3. **[Lesson 3]** - [Brief explanation]

### What We Discovered About You
1. **[Personal discovery 1]** - [Roast-style observation]
2. **[Personal discovery 2]** - [Roast-style observation]
3. **[Personal discovery 3]** - [Roast-style observation]

---

## 🔄 The Roast Cycle of Life

### Phase 1: Denial
*"This isn't that bad... right?"*

### Phase 2: Anger
*"Why is this roast so mean?! 😡"*

### Phase 3: Bargaining
*"Okay, I'll fix the templates, but leave the READMEs alone!"*

### Phase 4: Depression
*"My project really is a mess... 😭"*

### Phase 5: Acceptance
*"You know what, the roast was right. Let's fix this shit."*

### Phase 6: Enlightenment
*"My project is actually pretty good now! Thanks, roast master! 🙏"*

---

## 🎪 Final Roast Thoughts

### To The Project:
> [Final encouraging but still sassy message to the improved project]

### To The Developer:
> [Final encouraging message to the developer who survived the roast]

### To Future Projects:
> [Warning/wisdom for future projects]

---

## 🚀 What's Next?

### Immediate Actions
- [ ] Bask in the glory of your improved project
- [ ] Show off your new structure to colleagues
- [ ] Thank the roast master (optional but appreciated)

### Long-term Prevention
- [ ] Schedule regular roast sessions (quarterly?)
- [ ] Learn from these mistakes (don't repeat them!)
- [ ] Become a roast master yourself

### The Ultimate Goal
Transform from "Project Chaos" to "Project Excellence" - one roast at a time! 🎯

---

*This consolidation was created with ❤️, lots of 🔥, and just the right amount of 😏. Remember: Roasts hurt because they're true!*

## 📝 Roast Transcript Archive

For historical purposes and future reference, all three original roasts are preserved:

- `roast.md` - The Professional Approach
- `roast_by_opencode.md` - The Sassy Takedown
- `roast_gottlos.md` - The Brutal Truth Bomb

May they serve as both warning and inspiration! ⚠️✨
```

---

## 🎭 Style Guidelines

### Tone Variations

#### Professional Roast
- Direct but respectful
- Focus on technical debt
- Constructive criticism
- Industry best practices

#### Sassy Roast
- Sarcastic analogies
- Exaggerated comparisons
- Memes and humor
- Still technically accurate

#### Gottlose Roast
- No filter language
- Brutal honesty
- Self-correction when wrong
- Raw technical feedback

### Communication Patterns

#### Problem Presentation
```markdown
## 🔥 **PUNKT X: [Problem Title]**

**Das Problem:** [Clear description]

**Warum das scheiße ist:** [Impact explanation with analogy]

**Mein Fix-Vorschlag:** [Concrete solution]

**Bestätigst du das oder lehnst du ab?**
```

#### Confirmation Handling
- **If confirmed:** Execute fix immediately
- **If rejected:** Discuss alternative approaches
- **If partial:** Adapt solution to requirements

---

## 🛠️ Technical Implementation

### Required Tools
- File system operations (list, read, write, edit)
- Bash commands for bulk operations
- Git operations (if applicable)
- Template processing

### Error Handling
- Verify file operations before/after
- Backup critical files before changes
- Rollback procedures for each fix
- User confirmation for destructive operations

### Agent OS Integration

#### Context Management
```python
# Agent OS Spec Example
{
    "task_type": "guided_roast_session",
    "context_requirements": [
        "project_structure",
        "file_system_analysis",
        "user_interaction_history"
    ],
    "output_format": {
        "roast_files": ["roast.md", "roast_by_opencode.md", "roast_gottlos.md"],
        "change_log": "CHANGELOG.md",
        "task_summary": "task_summary.md"
    }
}
```

#### Learning Integration
- Track which problems are most common
- Learn from user preferences (which roast style works best)
- Build library of fix patterns
- Improve problem detection accuracy

---

## 📚 Template Library

### Common Anti-Patterns

#### 1. Template Duplication
**Detection:** Same filenames in multiple template directories
**Fix:** Consolidate to single location
**Rollback:** Copy back to original locations

#### 2. README Overdocumentation
**Detection:** Multiple README.md in subdirectories
**Fix:** Rename to specific purposes (GUIDE.md, MANUAL.md, SYSTEM.md)
**Rollback:** Rename back to README.md

#### 3. OS File Pollution
**Detection:** .DS_Store, Thumbs.db, *.tmp files
**Fix:** Delete + update .gitignore
**Rollback:** Git restore (if tracked)

#### 4. Directory Misplacement
**Detection:** Important directories (projects/, src/) at bottom
**Fix:** Reorganize hierarchy logically
**Rollback:** Move back to original positions

### Fix Templates

#### Template Consolidation
```bash
# Standard template consolidation
mkdir -p templates/
find . -name "*.template" -not -path "./templates/*" -exec cp {} templates/ \;
find . -name "templates" -not -path "./templates" -exec rm -rf {} \;
```

#### Documentation Organization
```bash
# Centralize documentation
mkdir -p docs/
find . -maxdepth 2 -name "README.md" -not -path "./README.md" -exec mv {} docs/ \;
```

---

## 🎯 Success Metrics

### Quantitative
- Number of problems identified vs solved
- Files reorganized
- Documentation improved
- Duplicate content eliminated

### Qualitative
- User understanding of changes
- Improved project maintainability
- Better development workflow
- Reduced technical debt

### Feedback Collection
```
Rate this session:
□ Very Helpful □ Helpful □ Neutral □ Not Helpful □ Waste of Time

What was most valuable?
[ ]

What could be improved?
[ ]
```

---

## 🔄 Continuous Improvement

### Template Evolution
- Update based on user feedback
- Add new anti-patterns as discovered
- Refine roast styles for effectiveness
- Improve fix automation

### Knowledge Base
- Build library of common project structures
- Document best practices for different tech stacks
- Create decision trees for problem solving
- Maintain pattern recognition database

---

*This template is designed to be used with Agent OS for consistent, effective project structure improvement sessions.*
