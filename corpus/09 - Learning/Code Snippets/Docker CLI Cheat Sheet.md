---
date: 2026-05-26
title: "Docker CLI Cheat Sheet"
tags: [learning, code-snippets, docker]
status: reference
type: note
---

title: Docker CLI Cheat Sheet
tags: #docker #dockerdesktop
date: 2025-06-03

---

Docker itself doesn't use a GUI-heavy interface with tons of keyboard shortcuts like Blender or Unity. Instead, it’s **CLI-first (command-line interface)** — but you can definitely create a **visual reference** for:

- ⚙️ Common `docker` CLI commands
    
- 🔁 Interactive flags
    
- 🧱 Building, starting, stopping containers
    
- 🧼 Cleanup and volume management
    
- 🧪 One-liner power commands (like starting Ubuntu shell, running NGINX, etc.)
    

---

## 🔧 Docker CLI Cheat Sheet (What We'll Graph)

### 🔹 Container Basics

```
docker run hello-world             # Test Docker install
docker run -it ubuntu              # Interactive shell
docker ps                          # List running containers
docker ps -a                       # List all containers (even exited)
docker stop [container_id]        # Stop a container
docker rm [container_id]          # Remove a container
docker rm $(docker ps -aq)        # Remove all containers
```

---

### 🔹 Images & Building

```
docker images                      # List all downloaded images
docker rmi [image_id]             # Remove image
docker build -t myimage .         # Build from Dockerfile
```

---

### 🔹 Volumes & Bind Mounts

```
docker run -v /host:/container    # Mount local folder into container
```

---

### 🔹 Docker Compose (if installed)

```
docker-compose up -d              # Start services
docker-compose down               # Stop & remove containers
```

---

### 🔹 Misc

```
docker logs [container_id]        # View logs
docker exec -it [id] bash         # Open bash in running container
docker network ls                 # List networks
```

---

## 🎨 Next Step:

I’ll now generate a **visual poster** for this — styled like your previous keyboard shortcut reference cards, but with:

- Command blocks
    
- Icons (container, shell, volume, etc.)
    
- Terminal theme
    

Let’s hit it.

## Links
[[Docker- Desktop]]
[[Related Project or Person]]

---

## Related Notes
- [[Code Completion like AutoCad]] - Shared code-snippets/learning focus
- [[Coding Shortcuts]] - Shared code-snippets/learning focus
- [[14_Key_Buildings_Reference_Sheet]] - Related learning topic
- [[4627-MAT-111-Original-Quiz-#2-Sheet]] - Related learning topic
- [[08.9 - Docker & Containers]] - Related docker topic
