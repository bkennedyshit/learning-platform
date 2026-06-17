---
title: "13.7 — Frontend with TypeScript: React, Vue, Svelte, SolidJS"
subject: "TypeScript"
catalog: advanced
audience_tier: higher-education
chapter: "13.7"
type: chapter
objectives:
  - "Understand the concepts"
  - "Apply the theory"
open_source: true
---

*Back to [Subject_Plan](Subject_Plan) | Part of [09 - Learning Index](09---Learning-Index)*

# 13.7 — Frontend with TypeScript: React, Vue, Svelte, SolidJS

> *"TypeScript doesn't just catch bugs in your components — it makes your components self-documenting. The types ARE the documentation."* — **Dan Abramov**, React Core Team

Every major frontend framework has first-class TypeScript support. This chapter covers the patterns you'll encounter in real codebases: typed props, generic components, typed hooks/composables, and framework-specific idioms. React gets the deepest coverage (it's the job market leader), but Vue, Svelte, and SolidJS patterns are included because you'll encounter them.

---

## 🎯 Learning Objectives

By the end of this chapter you will be able to:

1. Type React components (props, state, refs, events, children) with full generics support.
2. Write custom hooks with proper return type inference and overloads.
3. Understand React Server Components typing and the `"use client"` boundary.
4. Use Vue 3's `<script setup lang="ts">` with typed props, emits, and composables.
5. Apply TypeScript to Svelte 5 runes (`$state`, `$derived`, `$effect`).
6. Type SolidJS signals and derived computations.
7. Identify shared patterns across frameworks (typed props, events, stores).

---

## 🖼️ Visual Anchor — Framework TypeScript Integration

![ts__6.7-fig1](ts__6.7-fig1.svg)

---

## 📚 1. Concepts & Definitions

### Definition 13.7.1 — TSX (TypeScript JSX)

TSX is TypeScript's version of JSX. Files use `.tsx` extension. The compiler transforms JSX into function calls while type-checking props:

```tsx
// React component with typed props
interface ButtonProps {
  label: string;
  variant?: "primary" | "secondary" | "danger";
  disabled?: boolean;
  onClick: (event: React.MouseEvent<HTMLButtonElement>) => void;
}

function Button({ label, variant = "primary", disabled, onClick }: ButtonProps) {
  return (
    <button
      className={`btn btn-${variant}`}
      disabled={disabled}
      onClick={onClick}
    >
      {label}
    </button>
  );
}

// Usage — TypeScript validates all props:
<Button label="Submit" onClick={(e) => console.log(e.clientX)} />
// <Button label={42} />  // ❌ Error: number not assignable to string
// <Button />             // ❌ Error: missing required props
```

### Definition 13.7.2 — Generic Components

Components that accept a type parameter for flexible, reusable patterns:

```tsx
// Generic list component
interface ListProps<T> {
  items: T[];
  renderItem: (item: T, index: number) => React.ReactNode;
  keyExtractor: (item: T) => string;
  emptyMessage?: string;
}

function List<T>({ items, renderItem, keyExtractor, emptyMessage }: ListProps<T>) {
  if (items.length === 0) return <p>{emptyMessage ?? "No items"}</p>;
  return (
    <ul>
      {items.map((item, i) => (
        <li key={keyExtractor(item)}>{renderItem(item, i)}</li>
      ))}
    </ul>
  );
}

// Usage — T is inferred from items:
<List
  items={users}
  renderItem={(user) => <span>{user.name}</span>}  // user is typed as User
  keyExtractor={(user) => user.id}
/>
```

---

## 🔑 3. Mechanics — React + TypeScript

### 3.1 — Component Patterns

```tsx
// Pattern 1: Function component with destructured props
interface CardProps {
  title: string;
  children: React.ReactNode;
  footer?: React.ReactNode;
}

function Card({ title, children, footer }: CardProps) {
  return (
    <div className="card">
      <h2>{title}</h2>
      <div>{children}</div>
      {footer && <footer>{footer}</footer>}
    </div>
  );
}

// Pattern 2: Component with ref forwarding
interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label: string;
  error?: string;
}

const Input = React.forwardRef<HTMLInputElement, InputProps>(
  ({ label, error, ...props }, ref) => (
    <div>
      <label>{label}</label>
      <input ref={ref} {...props} />
      {error && <span className="error">{error}</span>}
    </div>
  )
);

// Pattern 3: Polymorphic component (renders as different elements)
type PolymorphicProps<E extends React.ElementType> = {
  as?: E;
  children: React.ReactNode;
} & Omit<React.ComponentPropsWithoutRef<E>, "as" | "children">;

function Box<E extends React.ElementType = "div">({
  as,
  children,
  ...props
}: PolymorphicProps<E>) {
  const Component = as || "div";
  return <Component {...props}>{children}</Component>;
}

// Usage:
<Box as="section" id="main">Content</Box>
<Box as="a" href="/about">Link</Box>
```

### 3.2 — Hooks with TypeScript

```tsx
// useState — type is inferred or explicit
const [count, setCount] = useState(0);           // number
const [user, setUser] = useState<User | null>(null); // explicit for nullable

// useRef — element refs vs mutable refs
const inputRef = useRef<HTMLInputElement>(null);  // DOM element ref
const timerRef = useRef<number>(0);              // Mutable value ref

// useReducer — typed actions with discriminated unions
type CounterAction =
  | { type: "increment"; amount: number }
  | { type: "decrement"; amount: number }
  | { type: "reset" };

interface CounterState {
  count: number;
  history: number[];
}

function counterReducer(state: CounterState, action: CounterAction): CounterState {
  switch (action.type) {
    case "increment":
      return { count: state.count + action.amount, history: [...state.history, state.count] };
    case "decrement":
      return { count: state.count - action.amount, history: [...state.history, state.count] };
    case "reset":
      return { count: 0, history: [] };
  }
}

const [state, dispatch] = useReducer(counterReducer, { count: 0, history: [] });
dispatch({ type: "increment", amount: 5 }); // ✅
// dispatch({ type: "increment" });          // ❌ missing 'amount'

// Custom hook with proper return type
function useLocalStorage<T>(key: string, initialValue: T) {
  const [stored, setStored] = useState<T>(() => {
    const item = localStorage.getItem(key);
    return item ? JSON.parse(item) : initialValue;
  });

  const setValue = (value: T | ((prev: T) => T)) => {
    const valueToStore = value instanceof Function ? value(stored) : value;
    setStored(valueToStore);
    localStorage.setItem(key, JSON.stringify(valueToStore));
  };

  return [stored, setValue] as const; // 'as const' for tuple return
}

// Usage:
const [theme, setTheme] = useLocalStorage<"light" | "dark">("theme", "light");
// theme: "light" | "dark"
// setTheme: (value: "light" | "dark" | ((prev) => ...)) => void
```

### 3.3 — React Server Components with TypeScript

```tsx
// Server Component (default in Next.js App Router)
// Can be async, can access server resources directly
interface PageProps {
  params: { id: string };
  searchParams: { page?: string };
}

// This runs on the server — no hooks, no browser APIs
export default async function UserPage({ params }: PageProps) {
  // Direct database access (no API call needed)
  const user = await db.user.findUnique({ where: { id: params.id } });

  if (!user) return <NotFound />;

  return (
    <div>
      <h1>{user.name}</h1>
      {/* Client component for interactivity */}
      <UserActions userId={user.id} />
    </div>
  );
}

// Client Component — must opt in with "use client"
"use client";

interface UserActionsProps {
  userId: string;
}

function UserActions({ userId }: UserActionsProps) {
  const [isFollowing, setIsFollowing] = useState(false);

  return (
    <button onClick={() => setIsFollowing(!isFollowing)}>
      {isFollowing ? "Unfollow" : "Follow"}
    </button>
  );
}

// Server Actions (typed form handling)
"use server";

async function updateProfile(formData: FormData): Promise<{ success: boolean }> {
  const name = formData.get("name") as string;
  await db.user.update({ where: { id: getCurrentUserId() }, data: { name } });
  return { success: true };
}
```


---

## 🔑 3 (continued). Mechanics — Vue 3 + TypeScript

### 3.4 — Vue 3 with `<script setup lang="ts">`

```vue
<!-- UserCard.vue -->
<script setup lang="ts">
import { ref, computed, onMounted } from "vue";

// Typed props (compiler macro — no import needed)
interface Props {
  userId: string;
  showAvatar?: boolean;
}

const props = withDefaults(defineProps<Props>(), {
  showAvatar: true,
});

// Typed emits
interface Emits {
  (event: "follow", userId: string): void;
  (event: "message", userId: string, text: string): void;
}

const emit = defineEmits<Emits>();

// Typed reactive state
interface User {
  id: string;
  name: string;
  avatar: string;
  followers: number;
}

const user = ref<User | null>(null);
const isLoading = ref(true);

// Typed computed
const displayName = computed(() => user.value?.name ?? "Unknown");

// Lifecycle with async
onMounted(async () => {
  const res = await fetch(`/api/users/${props.userId}`);
  user.value = await res.json();
  isLoading.value = false;
});

// Methods
function handleFollow() {
  if (user.value) {
    emit("follow", user.value.id);
  }
}
</script>

<template>
  <div v-if="isLoading">Loading...</div>
  <div v-else-if="user" class="user-card">
    <img v-if="showAvatar" :src="user.avatar" :alt="displayName" />
    <h3>{{ displayName }}</h3>
    <p>{{ user.followers }} followers</p>
    <button @click="handleFollow">Follow</button>
  </div>
</template>
```

### 3.5 — Vue Composables (Custom Hooks)

```ts
// composables/useFetch.ts
import { ref, type Ref } from "vue";

interface UseFetchReturn<T> {
  data: Ref<T | null>;
  error: Ref<Error | null>;
  isLoading: Ref<boolean>;
  refetch: () => Promise<void>;
}

export function useFetch<T>(url: string): UseFetchReturn<T> {
  const data = ref<T | null>(null) as Ref<T | null>;
  const error = ref<Error | null>(null);
  const isLoading = ref(true);

  async function refetch() {
    isLoading.value = true;
    error.value = null;
    try {
      const res = await fetch(url);
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      data.value = await res.json();
    } catch (e) {
      error.value = e instanceof Error ? e : new Error(String(e));
    } finally {
      isLoading.value = false;
    }
  }

  refetch();
  return { data, error, isLoading, refetch };
}
```

---

## 🔑 3 (continued). Mechanics — Svelte 5 + TypeScript

### 3.6 — Svelte 5 Runes with TypeScript

```svelte
<!-- Counter.svelte -->
<script lang="ts">
  // Svelte 5 runes — reactive primitives
  interface Props {
    initial?: number;
    step?: number;
    onCountChange?: (count: number) => void;
  }

  let { initial = 0, step = 1, onCountChange }: Props = $props();

  // $state — reactive variable (like ref() in Vue)
  let count: number = $state(initial);

  // $derived — computed value (like computed() in Vue)
  let doubled: number = $derived(count * 2);
  let isEven: boolean = $derived(count % 2 === 0);

  // $effect — side effect (like useEffect in React)
  $effect(() => {
    onCountChange?.(count);
  });

  function increment() {
    count += step;
  }

  function decrement() {
    count -= step;
  }
</script>

<div>
  <button onclick={decrement}>-</button>
  <span>{count} (doubled: {doubled}, {isEven ? "even" : "odd"})</span>
  <button onclick={increment}>+</button>
</div>
```

### 3.7 — Svelte 5 Typed Stores

```ts
// stores/user.svelte.ts
interface User {
  id: string;
  name: string;
  email: string;
}

class UserStore {
  current: User | null = $state(null);
  isAuthenticated: boolean = $derived(this.current !== null);

  async login(email: string, password: string): Promise<void> {
    const res = await fetch("/api/login", {
      method: "POST",
      body: JSON.stringify({ email, password }),
    });
    this.current = await res.json();
  }

  logout(): void {
    this.current = null;
  }
}

export const userStore = new UserStore();
```

---

## 🔑 3 (continued). Mechanics — SolidJS + TypeScript

### 3.8 — SolidJS Signals with TypeScript

```tsx
// SolidJS — fine-grained reactivity (no Virtual DOM)
import { createSignal, createMemo, createEffect, type Component } from "solid-js";

interface TodoItem {
  id: string;
  text: string;
  completed: boolean;
}

const TodoApp: Component = () => {
  // Signals — reactive primitives (like Vue ref, but no .value needed in JSX)
  const [todos, setTodos] = createSignal<TodoItem[]>([]);
  const [filter, setFilter] = createSignal<"all" | "active" | "completed">("all");

  // Memo — derived computation (only recalculates when dependencies change)
  const filteredTodos = createMemo(() => {
    const f = filter();
    const t = todos();
    switch (f) {
      case "all": return t;
      case "active": return t.filter(todo => !todo.completed);
      case "completed": return t.filter(todo => todo.completed);
    }
  });

  const remainingCount = createMemo(() =>
    todos().filter(t => !t.completed).length
  );

  // Effect — side effect that tracks dependencies automatically
  createEffect(() => {
    console.log(`${remainingCount()} items remaining`);
  });

  function addTodo(text: string) {
    setTodos(prev => [...prev, { id: crypto.randomUUID(), text, completed: false }]);
  }

  function toggleTodo(id: string) {
    setTodos(prev =>
      prev.map(t => t.id === id ? { ...t, completed: !t.completed } : t)
    );
  }

  return (
    <div>
      <h1>Todos ({remainingCount()} remaining)</h1>
      <For each={filteredTodos()}>
        {(todo) => (
          <div onClick={() => toggleTodo(todo.id)}>
            <span style={{ "text-decoration": todo.completed ? "line-through" : "none" }}>
              {todo.text}
            </span>
          </div>
        )}
      </For>
    </div>
  );
};
```

---

## 💻 4. Code Patterns & Examples

### Pattern 6.7.1 — Shared Patterns Across Frameworks

```ts
// All frameworks share these TypeScript patterns:

// 1. Typed Props Interface
interface SharedProps {
  title: string;
  items: Item[];
  onSelect: (item: Item) => void;
  variant?: "compact" | "expanded";
}

// 2. Generic Data Fetching Hook/Composable
interface UseQueryResult<T> {
  data: T | null;
  error: Error | null;
  isLoading: boolean;
  refetch: () => void;
}

// 3. Typed Event Handlers
type FormSubmitHandler = (data: FormData) => Promise<void>;
type ChangeHandler<T> = (value: T) => void;

// 4. Discriminated Union for Component State
type ComponentState<T> =
  | { status: "idle" }
  | { status: "loading" }
  | { status: "success"; data: T }
  | { status: "error"; error: Error };
```

---

## 🧮 5. Worked Examples

### Example 13.7.1 — Build a Type-Safe Form Hook (React)

<details>
<summary>🔍 View Step-by-Step Solution</summary>

```tsx
import { useState, useCallback, type ChangeEvent, type FormEvent } from "react";

interface UseFormOptions<T extends Record<string, unknown>> {
  initialValues: T;
  validate?: (values: T) => Partial<Record<keyof T, string>>;
  onSubmit: (values: T) => Promise<void>;
}

interface UseFormReturn<T extends Record<string, unknown>> {
  values: T;
  errors: Partial<Record<keyof T, string>>;
  isSubmitting: boolean;
  handleChange: (e: ChangeEvent<HTMLInputElement | HTMLSelectElement>) => void;
  handleSubmit: (e: FormEvent) => void;
  setFieldValue: <K extends keyof T>(field: K, value: T[K]) => void;
  reset: () => void;
}

function useForm<T extends Record<string, unknown>>({
  initialValues,
  validate,
  onSubmit,
}: UseFormOptions<T>): UseFormReturn<T> {
  const [values, setValues] = useState<T>(initialValues);
  const [errors, setErrors] = useState<Partial<Record<keyof T, string>>>({});
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleChange = useCallback((e: ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setValues(prev => ({ ...prev, [name]: value }));
    setErrors(prev => ({ ...prev, [name]: undefined }));
  }, []);

  const setFieldValue = useCallback(<K extends keyof T>(field: K, value: T[K]) => {
    setValues(prev => ({ ...prev, [field]: value }));
  }, []);

  const handleSubmit = useCallback(async (e: FormEvent) => {
    e.preventDefault();
    const validationErrors = validate?.(values) ?? {};
    if (Object.keys(validationErrors).length > 0) {
      setErrors(validationErrors);
      return;
    }
    setIsSubmitting(true);
    try {
      await onSubmit(values);
    } finally {
      setIsSubmitting(false);
    }
  }, [values, validate, onSubmit]);

  const reset = useCallback(() => {
    setValues(initialValues);
    setErrors({});
  }, [initialValues]);

  return { values, errors, isSubmitting, handleChange, handleSubmit, setFieldValue, reset };
}

// Usage:
function SignupForm() {
  const form = useForm({
    initialValues: { name: "", email: "", age: 0 },
    validate: (v) => {
      const errors: Partial<Record<keyof typeof v, string>> = {};
      if (!v.name) errors.name = "Required";
      if (!v.email.includes("@")) errors.email = "Invalid email";
      return errors;
    },
    onSubmit: async (values) => {
      await fetch("/api/signup", { method: "POST", body: JSON.stringify(values) });
    },
  });

  return (
    <form onSubmit={form.handleSubmit}>
      <input name="name" value={form.values.name} onChange={form.handleChange} />
      {form.errors.name && <span>{form.errors.name}</span>}
      <button disabled={form.isSubmitting}>Submit</button>
    </form>
  );
}
```

</details>

---

## ⚠️ 6. Gotchas & Anti-Patterns

### Gotcha 6.7.1 — React Event Types

```tsx
// ❌ Using generic Event type
function handleClick(e: Event) { /* ... */ }

// ✅ Use React-specific event types
function handleClick(e: React.MouseEvent<HTMLButtonElement>) {
  console.log(e.currentTarget.disabled); // typed!
}

function handleChange(e: React.ChangeEvent<HTMLInputElement>) {
  console.log(e.target.value); // string
}

function handleSubmit(e: React.FormEvent<HTMLFormElement>) {
  e.preventDefault();
}

// Common event types:
// React.MouseEvent<HTMLElement>
// React.ChangeEvent<HTMLInputElement>
// React.FormEvent<HTMLFormElement>
// React.KeyboardEvent<HTMLInputElement>
// React.FocusEvent<HTMLInputElement>
```

### Gotcha 6.7.2 — `children` Typing in React

```tsx
// ❌ Using 'any' for children
interface Props { children: any }

// ✅ Use React.ReactNode (accepts anything renderable)
interface Props { children: React.ReactNode }

// ✅ Use React.ReactElement for single component child
interface Props { children: React.ReactElement }

// ✅ Render prop pattern
interface Props { children: (data: User) => React.ReactNode }
```

### Gotcha 6.7.3 — `as const` for Hook Return Tuples

```tsx
// ❌ Without 'as const' — returns (string | Function)[]
function useToggle(initial: boolean) {
  const [value, setValue] = useState(initial);
  const toggle = () => setValue(v => !v);
  return [value, toggle]; // (boolean | (() => void))[]
}

// ✅ With 'as const' — returns [boolean, () => void]
function useToggle(initial: boolean) {
  const [value, setValue] = useState(initial);
  const toggle = () => setValue(v => !v);
  return [value, toggle] as const; // readonly [boolean, () => void]
}
```

---

## 🔗 7. Cross-links & Further Reading

### Internal Links
- **Previous:** [13.6 - Modules & Build Systems](13.6---Modules-&-Build-Systems)
- **Next:** [13.8 - Backend with TypeScript - Node, Bun, Deno, Express, Fastify, Hono](13.8---Backend-with-TypeScript---Node,-Bun,-Deno,-Express,-Fastify,-Hono)
- **React deep-dive:** [22.1 - React & Next.js - Functional Components & Hooks](22.1---React-&-Next.js---Functional-Components-&-Hooks)
- **Angular (heavy TS):** [22.2 - Angular - Class-based Architecture & RxJS](22.2---Angular---Class-based-Architecture-&-RxJS)

### External Resources
- [React TypeScript Cheatsheet](https://react-typescript-cheatsheet.netlify.app/)
- [Vue 3 TypeScript Guide](https://vuejs.org/guide/typescript/overview.html)
- [Svelte 5 TypeScript](https://svelte.dev/docs/typescript)
- [SolidJS TypeScript](https://www.solidjs.com/guides/typescript)
- [Total TypeScript — React with TypeScript](https://www.totaltypescript.com/tutorials/react-with-typescript)

---

*Last updated: 2026-05-24*



---

## 🏗️ 8. Modern Frontend Deep Dives: React 19, Vue Vapor, Svelte 5, SolidJS

### 8.1 — React 19: `use()` Hook & React Server Components

React 19 introduces the `use()` hook — a new primitive that can read promises and context inside render, enabling a fundamentally different data-fetching pattern.

#### The `use()` Hook

```tsx
import { use, Suspense } from "react";

// use() can read a Promise directly in render
function UserProfile({ userPromise }: { userPromise: Promise<User> }) {
  const user = use(userPromise); // Suspends until resolved!

  return (
    <div>
      <h1>{user.name}</h1>
      <p>{user.email}</p>
    </div>
  );
}

// Parent provides the promise and Suspense boundary
function App() {
  const userPromise = fetchUser("123"); // Start fetching immediately

  return (
    <Suspense fallback={<Skeleton />}>
      <UserProfile userPromise={userPromise} />
    </Suspense>
  );
}

// use() can also read Context conditionally (unlike useContext)
function ThemeButton({ showTheme }: { showTheme: boolean }) {
  if (showTheme) {
    const theme = use(ThemeContext); // ✅ Conditional! (useContext can't do this)
    return <button style={{ color: theme.primary }}>Themed</button>;
  }
  return <button>Default</button>;
}
```

#### React Server Components (RSC)

```tsx
// server-component.tsx — runs ONLY on the server
// No "use client" directive = server component by default

import { db } from "@/lib/database"; // Direct DB access!

async function UserList() {
  // This runs on the server — no API route needed
  const users = await db.query("SELECT * FROM users WHERE active = true");

  return (
    <ul>
      {users.map(user => (
        <li key={user.id}>
          {user.name}
          {/* Client components can be children of server components */}
          <LikeButton userId={user.id} />
        </li>
      ))}
    </ul>
  );
}

// client-component.tsx
"use client"; // This directive marks it as a client component

import { useState, useTransition } from "react";
import { likeUser } from "@/actions/users"; // Server Action

function LikeButton({ userId }: { userId: string }) {
  const [liked, setLiked] = useState(false);
  const [isPending, startTransition] = useTransition();

  return (
    <button
      disabled={isPending}
      onClick={() => {
        startTransition(async () => {
          await likeUser(userId); // Calls server action
          setLiked(true);
        });
      }}
    >
      {isPending ? "..." : liked ? "❤️" : "🤍"}
    </button>
  );
}
```

#### Server Actions (Form Handling)

```tsx
// actions/users.ts
"use server";

import { db } from "@/lib/database";
import { revalidatePath } from "next/cache";
import { z } from "zod";

const CreateUserSchema = z.object({
  name: z.string().min(2),
  email: z.string().email(),
});

export async function createUser(formData: FormData) {
  const parsed = CreateUserSchema.safeParse({
    name: formData.get("name"),
    email: formData.get("email"),
  });

  if (!parsed.success) {
    return { error: parsed.error.flatten() };
  }

  await db.insert("users", parsed.data);
  revalidatePath("/users");
  return { success: true };
}

// Usage in a form (works without JavaScript!)
function CreateUserForm() {
  return (
    <form action={createUser}>
      <input name="name" required />
      <input name="email" type="email" required />
      <button type="submit">Create User</button>
    </form>
  );
}
```

### 8.2 — Vue 3.4+ Vapor Mode

Vue Vapor Mode is an alternative compilation strategy that eliminates the Virtual DOM entirely, compiling templates directly to imperative DOM operations.

```tsx
// Standard Vue (VDOM-based)
// Template: <div>{{ count }}</div>
// Compiles to: h('div', null, count.value)  → VDOM diff → DOM patch

// Vapor Mode (no VDOM)
// Template: <div>{{ count }}</div>
// Compiles to:
//   const el = document.createElement('div')
//   const text = document.createTextNode('')
//   el.appendChild(text)
//   watchEffect(() => { text.nodeValue = count.value })
//   return el

// The result: ~50% smaller runtime, ~30% faster updates
```

#### Vapor Mode Component Example

```tsx
// VaporCounter.vue (opt-in per component)
<script setup vapor>
import { ref } from 'vue'

const count = ref(0)
const doubled = computed(() => count.value * 2)

function increment() {
  count.value++
}
</script>

<template>
  <div class="counter">
    <p>Count: {{ count }}</p>
    <p>Doubled: {{ doubled }}</p>
    <button @click="increment">+1</button>
  </div>
</template>
```

#### When to Use Vapor Mode

- **Use Vapor:** Performance-critical components, large lists, frequent updates
- **Use Standard:** Components with complex dynamic structures, heavy use of `<Transition>`, third-party VDOM-based libraries

### 8.3 — Svelte 5 Runes Deep Dive

Svelte 5 replaces the implicit reactivity system (`$:` labels, `let` assignments) with explicit **runes** — compiler-understood function calls that declare reactive state.

```tsx
// Svelte 4 (implicit reactivity — magic)
<script>
  let count = 0;           // Reactive because it's a top-level let
  $: doubled = count * 2;  // Reactive derived value (magic label)

  function increment() {
    count += 1;            // Assignment triggers reactivity
  }
</script>

// Svelte 5 (explicit runes — no magic)
<script>
  let count = $state(0);              // Explicitly reactive
  let doubled = $derived(count * 2);  // Explicitly derived

  function increment() {
    count += 1;  // Still triggers reactivity (rune tracks mutations)
  }
</script>
```

#### All Svelte 5 Runes

```tsx
<script>
  // $state — reactive state (replaces `let x = ...`)
  let name = $state("Bill");
  let items = $state<string[]>([]);

  // $state.raw — non-deeply-reactive state (for large objects)
  let bigData = $state.raw(fetchedData); // Only reassignment triggers update

  // $derived — computed values (replaces `$: x = ...`)
  let upper = $derived(name.toUpperCase());
  let total = $derived(items.reduce((sum, i) => sum + i.length, 0));

  // $derived.by — complex derivations with a function body
  let filtered = $derived.by(() => {
    const result = items.filter(i => i.startsWith("A"));
    return result.sort();
  });

  // $effect — side effects (replaces `$: { ... }` reactive statements)
  $effect(() => {
    console.log(`Name changed to: ${name}`);
    // Cleanup function (like React useEffect return)
    return () => console.log("Cleaning up previous effect");
  });

  // $effect.pre — runs before DOM update (like beforeUpdate)
  $effect.pre(() => {
    scrollContainer.scrollTop = scrollContainer.scrollHeight;
  });

  // $props — component props (replaces `export let`)
  let { title, count = 0, onUpdate } = $props<{
    title: string;
    count?: number;
    onUpdate: (value: number) => void;
  }>();

  // $bindable — two-way bindable props
  let { value = $bindable(0) } = $props<{ value?: number }>();
</script>

<input bind:value={name} />
<p>{upper}</p>
<p>Items: {total}</p>
```

### 8.4 — SolidJS Reactivity Primitives

SolidJS uses fine-grained reactivity (signals) with no Virtual DOM. Components run once; only the reactive expressions re-execute.

```tsx
import { createSignal, createEffect, createMemo, onCleanup, batch } from "solid-js";
import { render } from "solid-js/web";

function Counter() {
  // Signal: reactive atom (getter + setter)
  const [count, setCount] = createSignal(0);
  const [name, setName] = createSignal("Bill");

  // Memo: cached derived value (only recomputes when dependencies change)
  const doubled = createMemo(() => count() * 2);
  const greeting = createMemo(() => `Hello, ${name()}! Count: ${count()}`);

  // Effect: side effect that re-runs when dependencies change
  createEffect(() => {
    console.log(`Count is now: ${count()}`);
    // Cleanup runs before next execution
    onCleanup(() => console.log("Cleaning up previous effect"));
  });

  // Batch: group multiple updates into one re-render
  function reset() {
    batch(() => {
      setCount(0);
      setName("World");
    });
  }

  // JSX runs ONCE. Only the signal reads ({count()}) are reactive.
  return (
    <div>
      <p>{greeting()}</p>
      <p>Doubled: {doubled()}</p>
      <button onClick={() => setCount(c => c + 1)}>Increment</button>
      <button onClick={reset}>Reset</button>
    </div>
  );
}

render(() => <Counter />, document.getElementById("root")!);
```

#### SolidJS Stores (Nested Reactive State)

```tsx
import { createStore, produce } from "solid-js/store";

function TodoApp() {
  const [state, setState] = createStore({
    todos: [
      { id: 1, text: "Learn Solid", done: false },
      { id: 2, text: "Build app", done: false },
    ],
    filter: "all" as "all" | "active" | "done",
  });

  // Fine-grained updates: only affected DOM nodes re-render
  function toggleTodo(id: number) {
    setState("todos", todo => todo.id === id, "done", done => !done);
    // OR with produce (Immer-like API):
    setState(produce(s => {
      const todo = s.todos.find(t => t.id === id);
      if (todo) todo.done = !todo.done;
    }));
  }

  // Derived: only recomputes when todos or filter changes
  const filtered = createMemo(() => {
    switch (state.filter) {
      case "active": return state.todos.filter(t => !t.done);
      case "done": return state.todos.filter(t => t.done);
      default: return state.todos;
    }
  });

  return (
    <ul>
      <For each={filtered()}>
        {(todo) => (
          <li
            style={{ "text-decoration": todo.done ? "line-through" : "none" }}
            onClick={() => toggleTodo(todo.id)}
          >
            {todo.text}
          </li>
        )}
      </For>
    </ul>
  );
}
```

---

## 📎 9. Appendix — Deep Dives & Theory

### Appendix A — Signal-Based Reactivity vs VDOM Diffing

#### Virtual DOM (React, Vue standard mode)

```
State Change → Re-render Component → Generate New VDOM Tree
→ Diff Old vs New VDOM → Compute Minimal DOM Patches → Apply Patches

Complexity: O(n) where n = number of VDOM nodes in subtree
Memory: O(n) for the VDOM tree representation
```

**Advantages:**
- Simple mental model (re-render everything, framework figures out changes)
- Works well with immutable data patterns
- Batching is natural (collect all changes, diff once)

**Disadvantages:**
- O(n) diffing even when only one value changed
- Memory overhead of VDOM tree
- Reconciliation heuristics can be wrong (need `key` props)
- GC pressure from creating new VDOM objects every render

#### Signals (SolidJS, Svelte 5, Angular Signals, Vue Vapor)

```
Signal Value Changes → Notify Subscribed Effects/Computations
→ Re-execute ONLY the specific DOM binding → Direct DOM Update

Complexity: O(1) per signal change (only affected bindings update)
Memory: O(signals + subscriptions) — no VDOM tree
```

**Advantages:**
- O(1) updates — only affected DOM nodes change
- No diffing overhead
- No GC pressure from VDOM objects
- Predictable performance (no "death by a thousand re-renders")

**Disadvantages:**
- More complex mental model (must understand subscription graph)
- Potential for "glitches" (stale derived values during propagation)
- Debugging reactive graphs is harder than debugging render functions
- Less ecosystem tooling (React DevTools is more mature)

#### Performance Comparison (Realistic Benchmark)

```
Scenario: Update 1 item in a list of 10,000 items

React (VDOM):
  1. Re-render list component → generate 10,000 VDOM nodes
  2. Diff 10,000 nodes → find 1 change
  3. Apply 1 DOM patch
  Time: ~16ms (can drop frames)

SolidJS (Signals):
  1. Signal changes → notify 1 subscription
  2. Update 1 DOM text node
  Time: ~0.1ms (imperceptible)

React with memo/virtualization:
  1. Re-render list → memo blocks 9,999 children
  2. Re-render 1 child → generate 1 VDOM node
  3. Diff 1 node → apply 1 patch
  Time: ~2ms (requires manual optimization)
```

### Appendix B — React Compiler (React Forget) Auto-Memoization

React Compiler (formerly "React Forget") is an ahead-of-time compiler that automatically inserts `useMemo`, `useCallback`, and `React.memo` equivalents.

#### What It Does

```tsx
// YOUR CODE (no manual memoization):
function ProductList({ products, onSelect }) {
  const sorted = products.sort((a, b) => a.price - b.price);
  const total = products.reduce((sum, p) => sum + p.price, 0);

  return (
    <div>
      <p>Total: ${total}</p>
      {sorted.map(product => (
        <ProductCard
          key={product.id}
          product={product}
          onSelect={() => onSelect(product.id)}
        />
      ))}
    </div>
  );
}

// COMPILED OUTPUT (auto-memoized):
function ProductList({ products, onSelect }) {
  const sorted = useMemo(
    () => products.sort((a, b) => a.price - b.price),
    [products]
  );
  const total = useMemo(
    () => products.reduce((sum, p) => sum + p.price, 0),
    [products]
  );

  return (
    <div>
      <p>Total: ${total}</p>
      {sorted.map(product => (
        <ProductCard
          key={product.id}
          product={product}
          onSelect={useCallback(() => onSelect(product.id), [onSelect, product.id])}
        />
      ))}
    </div>
  );
}
```

#### How It Works Internally

1. **Static analysis** — The compiler builds a dependency graph of all values in the component
2. **Reactivity tracking** — It identifies which values depend on which props/state
3. **Memoization insertion** — It wraps computations in cache checks (similar to `useMemo`)
4. **Granular re-rendering** — Child components only re-render when their specific props change

#### Requirements for React Compiler

```ts
// ✅ Works with React Compiler:
// - Pure components (no side effects in render)
// - Hooks follow the Rules of Hooks
// - No mutation of props or state during render

// ❌ Breaks React Compiler:
function Bad({ items }) {
  items.push("new item"); // ❌ Mutating props!
  const ref = useRef(null);
  ref.current = "side effect"; // ⚠️ Ref mutation in render
  return <div>{items.length}</div>;
}
```

### Appendix C — Framework Reactivity Comparison Table

| Feature | React 19 | Vue 3.4 | Svelte 5 | SolidJS | Angular 17+ |
|---------|----------|---------|-----------|---------|-------------|
| Reactivity model | VDOM + Compiler | Proxy + VDOM/Vapor | Runes (signals) | Signals | Signals + zone.js (deprecated) |
| Component re-execution | Full re-render | Template re-render | Granular | Run once | Granular (signals) |
| State primitive | `useState` | `ref()`/`reactive()` | `$state()` | `createSignal()` | `signal()` |
| Derived values | `useMemo` | `computed()` | `$derived()` | `createMemo()` | `computed()` |
| Side effects | `useEffect` | `watch()`/`watchEffect()` | `$effect()` | `createEffect()` | `effect()` |
| SSR | RSC + Streaming | Nuxt SSR | SvelteKit SSR | Solid Start | Angular Universal |
| Bundle size (min) | ~40KB | ~33KB | ~2KB | ~7KB | ~45KB |
| TypeScript | First-class | First-class | First-class | First-class | First-class |

### Appendix D — Choosing a Frontend Framework (Decision Tree)

```
START
├── Need maximum ecosystem/jobs? → React
├── Need smallest bundle? → Svelte or SolidJS
├── Need best DX for full-stack? → Next.js (React) or SvelteKit
├── Coming from Angular/OOP background? → Vue or Angular
├── Need maximum runtime performance? → SolidJS
├── Building a widget/embed (size matters)? → Svelte or Preact
├── Enterprise with strict architecture? → Angular
└── Prototyping/MVP fast? → Vue or Svelte
```

---

*Last updated: 2026-05-24*
