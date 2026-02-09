# Skill: Ansible Playbook Creation

## Purpose
To automate server configuration.

## When to Use
- Tasks, handlers, and roles.
- When the specific requirement for Ansible Playbook Creation arises in the project.

## Procedure

### 1. Inventory Configuration
Define the target hosts in an `inventory.ini` or `inventory.yml` file.

```ini
[webservers]
web1.example.com ansible_host=192.168.1.10
web2.example.com ansible_host=192.168.1.11

[dbservers]
db1.example.com ansible_host=192.168.1.20
```

### 2. Creating a Playbook
Create a `site.yml` file to define the tasks for each group.

```yaml
---
- name: Configure Web Servers
  hosts: webservers
  become: yes # Run as root
  vars:
    http_port: 80
    max_clients: 200
  
  tasks:
    - name: Ensure Nginx is installed
      apt:
        name: nginx
        state: present
        update_cache: yes

    - name: Copy Nginx configuration
      template:
        src: templates/nginx.conf.j2
        dest: /etc/nginx/nginx.conf
      notify:
        - Restart Nginx

  handlers:
    - name: Restart Nginx
      service:
        name: nginx
        state: restarted
```

### 3. Using Roles for Scalability
Organize playbooks into roles for reusability.

```text
roles/
  common/
    tasks/main.yml
  webserver/
    tasks/main.yml
    templates/nginx.conf.j2
    handlers/main.yml
```

### 4. Running the Playbook
Use `ansible-playbook` to execute the automation.

```bash
# Check syntax
ansible-playbook site.yml --syntax-check

# Run the playbook
ansible-playbook -i inventory.ini site.yml
```

## Constraints
- **Idempotency**: Ensure tasks can run multiple times without changing the result if the system is already in the desired state.
- **Security**: Use `ansible-vault` to encrypt sensitive variables (passwords, API keys).
- **Modularity**: Break large playbooks into smaller roles.

## Expected Output
A set of YAML files that automatically configure remote servers to a desired state in a reproducible way.
