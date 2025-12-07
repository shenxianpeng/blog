```markdown
---
title: To Save Everyone Two Lines of Commands—I Packaged Gnuplot into an Out-of-the-Box Python Package
summary: |
  As an open-source project maintainer, I deeply understand the pain of "installing dependencies". To save users a couple of command lines, I spent time packaging gnuplot into an out-of-the-box Python package—gnuplot-wheel. This article shares the birth story and practical value of this little wheel.
tags:
  - gitstats
  - gnuplot
authors:
  - shenxianpeng
date: 2025-12-01
---

After coding for a long time, one inevitably develops a certain "paranoia."

One is a paranoia for **order**—unified naming, neat indentation, clean and crisp formatting.

The other is a paranoia for **simplicity**—the more automated, the better; the more out-of-the-box, the better; the more seamless, the better.

Especially when you're excitedly trying a new open-source project and hit enter after typing the installation command, what you expect to see is:

*   Lines of green progress bars
*   An easily understandable "Successfully installed"

Not:

*   A screen full of red errors
*   A cold, blunt message "Please install XXX system dependency first"

That feeling is like opening a takeout box when you're starving, only to find—

> **The restaurant forgot to give you chopsticks.**
> The food is right there, the aroma is wafting, but you just can't get it into your mouth.

This sense of frustration is a common pain for all developers.

Recently, while maintaining my own open-source project, I was deeply bothered by these "chopsticks."
To thoroughly solve it, I simply... built a new "wheel."

Today, let's talk about the story behind it.

---

## **The Genesis: gitstats and its Only "Less Smooth" Aspect**

I've been maintaining a tool called [**gitstats**](https://github.com/shenxianpeng/gitstats), primarily used to generate statistical reports for Git repositories:

*   Commit activity
*   Contributor ranking
*   Project growth trends
*   Graphical visualization

It's open-source, simple, and easy to use—except for one point:
**It depends on gnuplot.**

[gnuplot](http://www.gnuplot.info/) is a very mature plotting tool, commonly found in scientific research and data analysis.

The problem is: it must be installed manually at the system level.

Linux requires `apt install`;
macOS requires `brew install`;
Windows... you know, it's even more troublesome.

This is like the only grain of sand in the process, making the whole experience less smooth.

I started thinking:
**Can gnuplot be made into a Python package, installable with a single `pip install` command?**

*   No administrator privileges required
*   Does not pollute the system environment
*   Automatically adapts whether you're on Linux / Windows / macOS
*   Runs as long as Python is available

This way, developers can include gnuplot just like installing any ordinary Python package.

---

## **Thus, gnuplot-wheel was Born**

After some research and effort, I finally packaged **gnuplot's binary files into Python wheel files.**

From now on, you just need to type:

```bash
pip install gnuplot-wheel
```

*   gnuplot's binary files will be automatically installed into the virtual environment
*   No system-level dependencies required
*   Will not conflict with already installed gnuplot
*   No administrator privileges required

After installation, you can directly execute the `gnuplot` command—
**without installing anything extra.**

When I first saw it running smoothly in a clean environment, I had only one thought:

> **Ah, this is the romance of technology—keeping the complexity for oneself, and simplicity for the user.**

---

## **Who Will Use This Little Wheel?**

Actually, this wheel isn't complex, but it's very practical.

### **If You Work in Scientific Research or Data Visualization**

You can directly call gnuplot within your Python programs, without bothering with system dependencies.

### **If You Work in DevOps or Automation**

You can have your scripts automatically render curve plots and trend graphs, without having to manually install gnuplot on every machine.

### **If You Are Developing Tools That Depend on gnuplot (Like Me)**

You can directly add `gnuplot-wheel` to your dependencies, making it zero-cost for users to get started.

Currently, `gnuplot-wheel` supports mainstream platforms and is published on **PyPI**.

---

## **This "Little Wheel" Also Benefited gitstats**

I have already integrated it into gitstats.

Now, the latest version of gitstats no longer requires users to manually install gnuplot.

As long as:

```bash
pip install gitstats
```

It will automatically prepare all dependencies, and users don't need to care about what's happening behind the scenes.

This is the most charming aspect of the open-source community:

> **I built a 'back scratcher' to solve my own little pain point, and it turned out it could help others relieve their itching too.**

---

## **Want to Give It a Try?**

If your project, workflow, or script needs to use gnuplot, why not give it a try?
It won't change the world, but it can make your development process—**just a little bit smoother.**

Project links:

*   GitHub: [https://github.com/shenxianpeng/gnuplot-wheel](https://github.com/shenxianpeng/gnuplot-wheel)
*   PyPI: [https://pypi.org/project/gnuplot-wheel/](https://pypi.org/project/gnuplot-wheel/)

Feel free to check it out, use it, open an Issue, or even contribute together.

---

Please credit the author and source when reprinting articles from this site. Do not use for any commercial purposes. Welcome to follow the official account "DevOps攻城狮"
```