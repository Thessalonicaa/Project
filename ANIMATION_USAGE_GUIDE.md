## 🎨 How to Use Animations in Your Components

### **Quick Start**

All animations are already loaded globally. Just add the class names to your elements!

---

## **1️⃣ Entrance Animations**

### **Float Up (Default)**
```vue
<div class="animate-float">
  Content appears floating up
</div>
```

### **Slide from Right**
```vue
<div class="animate-slide-right">
  Slides in from right side
</div>
```

### **Slide from Left**
```vue
<div class="animate-slide-left">
  Slides in from left side
</div>
```

### **Pop In**
```vue
<div class="animate-pop">
  Bounces in with rotation
</div>
```

### **Zoom**
```vue
<div class="animate-zoom">
  Scales in from small to full
</div>
```

### **Rotate**
```vue
<div class="animate-rotate">
  Rotates while fading in
</div>
```

---

## **2️⃣ Continuous Animations**

### **Pulsing Glow**
```vue
<div class="animate-pulse-glow">
  Glows pulsing in and out
</div>
```

### **Neon Border**
```vue
<div class="animate-neon-border border-2 border-red-500">
  Border pulses between red and cyan
</div>
```

### **Neon Text**
```vue
<h1 class="animate-neon text-neon">
  Text glows with neon effect
</h1>
```

### **Shimmer**
```vue
<div class="animate-shimmer h-12">
  Loading shimmer effect
</div>
```

### **Glitch**
```vue
<span class="animate-glitch">
  Text flickers glitch effect
</span>
```

---

## **3️⃣ Hover Effects**

### **Lift on Hover**
```vue
<div class="hover-lift">
  Lifts up and shadows on hover
</div>
```

### **Glow on Hover**
```vue
<div class="hover-glow">
  Glows red/cyan on hover
</div>
```

### **Scale on Hover**
```vue
<button class="hover-scale">
  Grows 5% when hovered
</button>
```

---

## **4️⃣ Stagger Animations**

### **Sequential Item Animations**
```vue
<div>
  <div v-for="item in items" :key="item" class="stagger-child">
    {{ item }}
  </div>
</div>
```
- Item 1: appears at 0.1s
- Item 2: appears at 0.2s
- Item 3: appears at 0.3s
- ... up to 8 items

---

## **5️⃣ Text Effects**

### **Neon Text**
```vue
<h1 class="text-neon">
  Red text with red glow
</h1>
```

### **Cyan Neon**
```vue
<h2 class="text-neon-cyan">
  Cyan text with cyan glow
</h2>
```

### **Gradient Text**
```vue
<p class="text-gradient">
  Red → Pink → Cyan gradient
</p>
```

---

## **6️⃣ Card Styles**

### **Neon Card**
```vue
<div class="card-neon">
  Card with animated border
</div>
```

### **With Hover**
```vue
<div class="card-neon hover-lift">
  Lifts and glows on hover
</div>
```

### **With Glow Effect**
```vue
<div class="glow-effect">
  Animated glow around card
</div>
```

---

## **7️⃣ Button Styles**

### **Neon Button**
```vue
<button class="btn-neon">
  Neon border with sweep effect
</button>
```

### **With Animations**
```vue
<button class="btn-neon hover-lift animate-bounce">
  <i class="fas fa-rocket animate-spin"></i>
  Action
</button>
```

---

## **8️⃣ Icon Animations**

### **Spinning**
```vue
<i class="fas fa-spinner animate-spin"></i>
```

### **Bouncing**
```vue
<i class="fas fa-arrow-down animate-bounce"></i>
```

### **Pulsing**
```vue
<i class="fas fa-heart animate-pulse-glow"></i>
```

---

## **9️⃣ Background Effects**

### **Grid Pattern**
```vue
<div class="bg-grid">
  Grid pattern background
</div>
```

### **Dot Pattern**
```vue
<div class="bg-dots">
  Dot pattern background
</div>
```

### **Loading State**
```vue
<div class="loading h-20">
  Shimmer loading effect
</div>
```

---

## **🔟 Badges**

### **Red Badge**
```vue
<span class="badge badge-red">
  NEW
</span>
```

### **Cyan Badge**
```vue
<span class="badge badge-cyan">
  HOT
</span>
```

---

## **📝 Real Component Examples**

### **Hero Section**
```vue
<div class="min-h-screen bg-dark-bg flex items-center justify-center">
  <div class="text-center space-y-6">
    <h1 class="text-5xl font-bold text-neon animate-neon animate-float">
      Welcome
    </h1>
    <p class="text-xl text-gradient animate-slide-up">
      Futuristic Design System
    </p>
    <button class="btn-neon hover-lift animate-bounce">
      Get Started
    </button>
  </div>
</div>
```

### **Card Grid**
```vue
<div class="grid grid-cols-1 md:grid-cols-3 gap-6">
  <div 
    v-for="(item, i) in items" 
    :key="i" 
    class="stagger-child card-neon hover-lift animate-fade-scale"
  >
    <h3 class="text-lg text-neon">{{ item.title }}</h3>
    <p class="text-gray-400">{{ item.description }}</p>
  </div>
</div>
```

### **Form Input**
```vue
<input
  v-model="search"
  type="text"
  placeholder="Search..."
  class="w-full px-4 py-2 rounded-lg bg-gray-900/80 border-2 border-red-500/30 text-white focus:border-red-500 focus:ring-4 focus:ring-red-500/20 hover-glow"
/>
```

### **Navigation Menu**
```vue
<nav class="space-y-2">
  <NuxtLink
    v-for="item in menu"
    :key="item"
    :to="item.path"
    class="menu-item stagger-child hover-lift animate-fade-scale"
  >
    <i :class="item.icon" class="mr-3 animate-spin"></i>
    {{ item.name }}
  </NuxtLink>
</nav>
```

---

## **💡 Pro Tips**

### **Tip 1: Combine Multiple Animations**
```vue
<div class="animate-float hover-lift card-neon animate-neon-border">
  Multiple effects combined
</div>
```

### **Tip 2: Delay Animations**
```css
.delay-100 { animation-delay: 100ms; }
.delay-200 { animation-delay: 200ms; }
```

### **Tip 3: Reduce Motion Accessibility**
```css
@media (prefers-reduced-motion: reduce) {
  * { animation: none !important; }
}
```

### **Tip 4: Custom Duration**
```css
.animate-slow { animation-duration: 2s; }
.animate-fast { animation-duration: 0.3s; }
```

---

## **🎯 Animation Checklist**

Use this checklist when building components:

- [ ] Page entrance: `animate-float`, `animate-slide-*`, or `animate-pop`
- [ ] Cards: `card-neon` + `hover-lift` + `animate-fade-scale`
- [ ] Buttons: `btn-neon` or gradient + `hover-lift`
- [ ] Icons: `animate-spin`, `animate-bounce`, or `animate-pulse`
- [ ] Text: `text-neon`, `text-gradient`, or `animate-glitch`
- [ ] Lists: Use `stagger-child` for sequential items
- [ ] Hover states: Add `hover-glow`, `hover-scale`, or `hover-lift`
- [ ] Loading: Use `animate-shimmer` or `loading` class
- [ ] Borders: Use `animate-neon-border` for animated borders

---

## **🚀 Next Steps**

1. **Update Navbar** - Add animations to all menu items
2. **Update Cards** - Add `card-neon` and `hover-lift` to cards
3. **Update Forms** - Add hover and focus animations
4. **Update Buttons** - Use `btn-neon` or gradient styles
5. **Update Modals** - Add entrance animations
6. **Update Lists** - Use `stagger-child` for items

---

## **✅ All Set!**

Your frontend now has:
- ✅ 20+ animations ready to use
- ✅ Consistent dark-red theme
- ✅ Hover effects everywhere
- ✅ Stagger system for lists
- ✅ Professional animations
- ✅ Futuristic design

**Just add the classes to your components!** 🎉