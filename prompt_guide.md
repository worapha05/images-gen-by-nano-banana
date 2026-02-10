# AI Image Generation Prompt Guide

## Overview
This guide explains how the AI Image Generation API automatically constructs prompts for creating educational illustrations based on different input scenarios.

---

## Quick Decision Tree
```
Has Uploaded Images?
├─ YES
│  ├─ Has Custom Prompt?
│  │  ├─ YES → Use Reference + Custom Template
│  │  └─ NO → Use Reference Only Template
│  └─ [Adapt for 1 or Multiple Images]
└─ NO
   ├─ Has Custom Prompt?
   │  ├─ YES → Use Custom Prompt Template
   │  └─ NO → Use Random Default Prompt (8 options)
```

---

## Prompt Generation Logic

The system automatically generates educational-focused prompts based on whether images are uploaded and whether custom prompts are provided.

### 1. With Uploaded Images + Custom Prompt

**Single Image:**
```
Using the uploaded image as reference, create an educational illustration: {user_prompt} Include educational elements like classrooms, books, students, teachers, learning materials, or academic settings while maintaining the visual style of the reference image.
```

**Multiple Images:**
```
Using the {image_count} uploaded images as references, create an educational illustration: {user_prompt} Combine visual styles from all images and integrate educational themes like learning environments, educational materials, students, teachers, and academic activities.
```

### 2. With Uploaded Images + No Custom Prompt

**Single Image:**
```
Transform this image into an educational context. Add educational elements like books, students, teachers, desks, whiteboards, learning materials, or classroom settings while maintaining the original style and composition.
```

**Multiple Images:**
```
Using these {image_count} images as inspiration, create an educational illustration that combines elements from all references. Include learning environments, educational materials, students engaged in learning activities, and academic settings.
```

### 3. No Images + Custom Prompt
```
Create an educational illustration: {user_prompt} Include learning environments (classroom, library, lab), educational materials (books, computers, supplies), and students or teachers in learning activities.
```

### 4. No Images + No Custom Prompt (Default Prompts)

The system randomly selects from these 8 pre-defined educational prompts:

#### Default Prompt:

1. **Modern Classroom**
   ```
   Create a modern classroom with diverse students learning together, educational posters on walls, books on shelves, and a teacher facilitating discussion. Bright and inspiring atmosphere.
   ```

2. **Study Desk**
   ```
   Generate a student's study desk with open textbooks, notebooks, laptop, pens, desk lamp, and coffee mug. Include motivational elements and organized learning materials.
   ```

3. **Tree of Knowledge**
   ```
   Create an educational concept showing books transforming into a tree of knowledge with different subjects as branches (science, math, art, language). Students exploring and light bulbs representing ideas.
   ```

4. **Learning Space**
   ```
   Design a learning space with reading corner, group study area, computers, and presentation zone. Show diverse students learning in different ways with educational displays.
   ```

5. **Library Scene**
   ```
   Generate a beautiful library with bookshelves, reading nooks, study tables with focused students, natural lighting, and peaceful learning atmosphere.
   ```

6. **Science Lab**
   ```
   Create a science lab with students conducting experiments, microscopes, safety equipment, colorful chemicals, educational posters, and teacher guiding discovery learning.
   ```

7. **Art Classroom**
   ```
   Design an art classroom with students creating artwork, easels, art supplies, displayed student work, and instructor demonstrating techniques. Creative and inspiring environment.
   ```

8. **Outdoor Education**
   ```
   Generate an outdoor education scene with students and teachers in nature, observing plants and insects, taking notes, using magnifying glasses, and learning about ecosystems.
   ```