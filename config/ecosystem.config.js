module.exports = {
  apps: [{
    name: "AliBot",
    script: "AliBot/main.py",
    interpreter: "/usr/bin/python3.10",
    watch: ["AliBot/main.py","AliBot/cogs/", "AliBot/utils/"],
    ignore_watch: ["AliBot/cogs/__pycache__", "AliBot/utils/__pycache__"]
  }, {
    name: "HugBot",
    script: "HugBot/main.py",
    interpreter: "/usr/bin/python3.10",
    watch: ["HugBot/main.py","HugBot/cogs/", "HugBot/utils/"],
    ignore_watch: ["HugBot/cogs/__pycache__", "HugBot/utils/__pycache__"]
  }, {
    name: "TestBot",
    script: "TestBot/main.py",
    interpreter: "/usr/bin/python3.10",
    // watch: ["TestBot/main.py","TestBot/cogs/", "TestBot/utils/"],
    // ignore_watch: ["TestBot/cogs/__pycache__", "TestBot/utils/__pycache__"]
  }, {
    name: "TestBot2",
    script: "TestBot2/main.py",
    interpreter: "/usr/bin/python3.10",
    // watch: ["TestBot2/main.py","TestBot2/cogs/", "TestBot2/utils/"],
    // ignore_watch: ["TestBot2/cogs/__pycache__", "TestBot2/utils/__pycache__"]
  }]
}
