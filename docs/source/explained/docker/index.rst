.. Author: Akshay Mestry <xa@mes3.dev>
.. Created on: Saturday, 30 August 2025
.. Last updated on: Thursday, 4 September 2025

:og:title: Learning Docker
:og:description: Begineer's guide to Docker and containerisation
:og:type: article
:og:image: https://raw.githubusercontent.com/xames3/smart/main/docs/source/
    assets/opengraph/it-works-on-my-machine-meme.jpg

.. _explained-learning-docker:

===============================================================================
:octicon:`container` Learning Docker
===============================================================================

.. author::
    :name: Akshay Mestry
    :email: xa@mes3.dev
    :about: National Louis University
    :avatar: https://avatars.githubusercontent.com/u/90549089?v=4
    :github: https://github.com/xames3
    :linkedin: https://linkedin.com/in/xames3
    :timestamp: 30 Aug, 2025

.. rst-class:: lead

    See... it works on my machine!

This is my story from September 2020, roughly five years ago as of writing this
article. It is amidst the pandemic while I was switching jobs. I knew I would
get a new machine from my next employer, but I had no idea when. The pandemic
was still at its peak, and I had to make the most of what I had. With how
things were going, I knew I wouldn't get a new machine anytime soon, so I had
to improvise and make my work machine last me a while longer.

As some of you know, I love writing code. It's what I do for the most part, and
during lockdown, I wrote a lot! I tried to keep myself busy with work and other
side projects, and while doing that, I got my machine messy really quick. I had
multiple versions of Python, Rust, various dependencies, configs, tools, and
frameworks that I won't be using after my *"experimentation"* phase. I knew
`Docker`_ was a thing, but I never really got around to using it. I personally
thought it was too much of a hassle to set up until I had no other option. So,
I decided to give it a try.

And here we are today...

.. _but-what-is-docker:

-------------------------------------------------------------------------------
But what is Docker?
-------------------------------------------------------------------------------

Learning and exploring Docker wasn't initially on my bingo list, but I'm glad I
did. Since then, it has made my hacky projects super duper manageable, and my
local machine still thanks me for it! I don't want to get too technical or
nerdy right now, but I want to make sure we're on the same page. Docker is a
**platform** that allows you to develop, ship, and run code inside
`containers`_.

Simply put, it's basically a service that allows you to ship your application
or code in a container that has all the things it needs to run. This means your
application or code will run the same way regardless of where it's being run.
You'll get the same results on your local machine, your friend's machine, or a
server in the cloud.

It solves the classic "it works on my machine" problem.

.. note::

    Docker is not the only containerisation platform, but it's perhaps the most
    popular one and that's why people synonymously use the term Docker to refer
    to containers in general. But in reality, they are not the same thing.

Docker was introduced in 2013 and has evolved since then. In the spirit of
keeping things simple, I'd say there are two main components to Docker:
`Docker Engine`_ and `Docker Hub`_, and let's just stick with these two for
now.

1. **Docker Engine.** This is the core part of Docker that runs on your
   machine. It creates and manages containers. In a nutshell, it's the main
   thing that makes Docker work on your machine. Like how Git is the tool
   that makes version control possible, Docker Engine is the tool that makes
   containerisation possible.

   .. picture:: ../../assets/coloured/docker-engine-internals
       :alt: Docker Engine Internals

       Inside the Docker Engine. The commands you run on your terminal go to
       the Docker CLI which acts as a client to the Docker Daemon (dockerd)
       that runs in the background. Docker Daemon is the server-side part of
       the Docker Engine that does all the heavy lifting.

2. **Docker Hub.** This is a cloud-based registry service where you can find
   and share container images. Again, you can think of it as a GitHub or GitLab
   for Docker images. You can pull images from Docker Hub to run containers on
   your local machine, or you can push your own images to Docker Hub to share
   them with others.

.. _magic-of-docker-engine:

-------------------------------------------------------------------------------
Magic of Docker Engine
-------------------------------------------------------------------------------

This is my personal take on the Docker Engine but it helps to explain what it
is. Being a huge cinephile, I like to think of it as a movie production crew.
You don't see them on screen, but without them, nothing would work. They're the
ones who are setting up the lights, managing the cameras, and making sure
everything runs smoothly behind the scenes. In that same way, the engine runs
everything behind the scenes.

When I first started using Docker, I'll be honest, I really didn't understand
what was going on. Almost every tutorial I watched started with using
:console:`$ docker run` command and I knew that I could type it out and
auto-magically, I'm dropped in an isolated environment where I can run my code
or do whatever I want without messing up my local machine. It was like having
a personal sandbox to play in.

Want to try out the latest RC build of Python? No problem, run...

:console:`$ docker run -it python:3.14.0rc2 python`

Want to test out new features of Postgres without installing it globally? Easy,
run...

:console:`$ docker run -p 5432:5432 -e POSTGRES_PASSWORD=password -d postgres`

Want to test out my new Rust project without worrying about breaking my
existing Rust setup? Done, run...

:console:`$ docker run -it rust cargo new rustorch --bin`

I was sold!!

But as I started using it more, I realised that there's a lot more to it, and
Docker Engine is doing some really fancy stuff behind the scenes. Remember how
I mentioned my machine was getting messy with all the different versions of
Python and other dependencies? Well, when I ran :console:`$ docker run`
command, it was Docker Engine that was creating an isolated environment to run
my experiments within it.

These environments are what we call as **containers**.

.. _idea-behind-containers:

-------------------------------------------------------------------------------
Idea behind Containers
-------------------------------------------------------------------------------

In 1950s, `Malcolm McLean`_ came up with the concept of "containerisation" by
inventing and standardising the modern shipping containers, but his idea was
to make shipping goods easier and more efficient. Essentially, what it all
meant was that instead of loading and unloading goods every time they were
transferred from one mode of transport to another, they could be packed into a
standardised container that could be easily moved around.

Docker, the company took this idea and applied it to software development. The
name "Docker" itself is inspired by the idea of shipping containers. A
container is essentially a lightweight, standalone package that includes
everything needed to run your application code, runtime, system tools,
libraries, and settings. It's like having a perfectly sealed but fully equipped
sandbox that you can play in without worrying about the mess spilling over to
your actual backyward. Each container is isolated from the others and from the
host system, which means you can run multiple containers on the same machine
without them interfering with each other.

.. _containers-are-not-vms:

-------------------------------------------------------------------------------
Containers are not VMs!
-------------------------------------------------------------------------------

Initially, it was quite hard for me to wrap my head around the concept of
containers and sandboxing. I mean, how is it any different from a GUI-less
`Virtual machine`_? It's essentially acting the same way, right? Well, not
exactly. Virtual machine (VMs) and containers are both used to create isolated
environments, but they do it in different ways. VMs run a full copy of an
operating system (guest) inside your local machine (host), while containers
shares your host OS kernel.

.. admonition:: :fas:`sparkles` Quick analogy
    :class: unusual-one hint

    Think of it this way, having a VM is like renting an entire apartment when
    you just need a room, while using a container is like renting a room in a
    shared apartment where you share some common facilities like the kitchen
    and bathroom. The latter is much more fast, efficient, and cost-effective.

To expand a bit more, a VM creates a complete separate copy of an operating
system on top of your existing OS using something called as a `Hypervisor`_.
Note that is **not** dual-booting where you have two OSes installed on your
machine and you choose which one to boot into. In a VM, you have your main OS
(host) running, and inside it, you have another OS (guest) running as a
separate entity. VMs run like a regular application on your local machine. It's
like running Windows on your Mac using `Parallels`_ or like running Linux on
your Windows using `VirtualBox`_.

Since a VM runs just like a regular application, it needs its own set of
dedicated resources like CPU, memory, storage, and processing power. It's
thorough, but it's also heavy. Very heavy... I mean, you're running multiple
OSes at the same time!

.. picture:: ../../assets/coloured/vm-on-host
    :alt: Virtual Machine on a host MacBook Pro

    Virtualisation using Virtual Machines. Here, the MacBook Pro represents the
    physical hardware (Infrastructure). On top of that, we have macOS which is
    the host operating system. Then we have Parallels which is the Hypervisor
    application that creates and manages the VMs. Inside Parallels, we have a
    Windows 11 VM, macOS 26 VM, and an Ubuntu 24.04 VM running as separate
    guest OSes. These VMs have their own executables, libraries, and binaries
    which assist in running the Python 3.10 interpreter.

Containers, on the other hand, share the host OS's resources (kernel) and run
as isolated processes (not technically) in user space on the host OS. In simple
terms, they are much more lightweight and efficient compared to VMs. They start
up quickly and use fewer resources because they don't need to boot up a full
OS. You can run many more containers on the same hardware compared to VMs. This
makes containers ideal for deploying applications in a microservices
architecture where you have multiple small, independent services running
together.

.. picture:: ../../assets/coloured/container-on-host
    :alt: Container on a host MacBook Pro

    Containerisation using Docker. Here, the MacBook Pro represents the
    physical hardware (Infrastructure). On top of that, we have macOS which is
    the host operating system. Then we have Docker (Container Engine) which is
    the software that creates and manages containers. Inside Docker, we have
    multiple containers running isolated Python 3.10 interpreters, each with
    their own binaries and libraries but all sharing the same host OS kernel
    and resources.

.. _pulling-images-from-docker-hub:

-------------------------------------------------------------------------------
Pulling images from Docker Hub
-------------------------------------------------------------------------------

Okay, coming back to my story... this is me a few days into getting started
with Docker. After understanding what containers do and how they're better in
comparison to VMs, I realised why Docker is so popular among developers. I was
already using it for my personal projects. But now I had another problem... I
had a messy local machine with multiple Docker containers with the same Python
versions. I realised I needed to clean up and manage my containers better, or
follow some best practices. In doing so, I wondered where I had been getting
all these containers from in the first place. That's when I discovered
**Docker Hub**.

I thought I was downloading these containers from the internet, but I had no
idea where. It turns out that Docker Hub is a cloud-based registry service
where you can find and share container images, not containers! And that got me
confused all over again. I mean, I got the concept of containers, but what's an
image now? With a bit of research, I found out that a Docker image is a
lightweight, standalone, and executable package that includes everything needed
to run a piece of software, including the code, runtime, libraries, environment
variables, and configuration files. Wait, that sounds a lot like a container to
me.

But not quite...

An image is a blueprint for creating containers. When you run a Docker image,
it creates a container based on that image. It is a read-only template that
contains the instructions for creating a container. You can think of it as a
snapshot of a filesystem and settings to run an application. You can have
multiple containers running from the same image, each with its own isolated
environment.

.. admonition:: :fas:`sparkles` Quick analogy
    :class: unusual-one hint

    In programming terms, you can think of an image as a class and a container
    as an instance of that class. You can have multiple containers (instances)
    running from the same image (class) at the same time.

And Docker Hub is where you can find and share these images. You can pull
images from Docker Hub to run containers on your local machine, or you can push
your own images to Docker Hub to share them with others. Docker Hub has a vast
library of pre-built images for various applications and services, including
databases, web servers, programming languages, and more. This makes it easy to
get started with Docker and quickly set up your development environment.

Yet another reason why Docker is so popular among developers...

.. _a-week-into-docker:

-------------------------------------------------------------------------------
A week into Docker
-------------------------------------------------------------------------------

By now, I was a week into using Docker, and I was totally hooked! I had a basic
understanding of what Docker and containerisation are and roughly how the whole
ecosystem works. I was excited to explore and experiment even more. Sure, I was
confused in the beginning, but I slowly started to get the hang of it. First,
it was between containers and virtual machines, then with containers and
images. I think the biggest culprits were the terminologies themselves. They
are so similar that it can get really confusing for a beginner.

But once I got the hang of it, I realised how powerful the whole concept of
containerisation is and how it can make my life easier. After a few weeks, I
realised that even containerisation isn't a new concept. It's been around and
experimented with for decades within the Linux community. There are other
containerisation implementations like `LXC`_ and `OpenVZ`_, but Docker made it
easy and accessible for everyone.

In the next chapter, I'll share my experiences of running my first container
and how it changed the way I started working on my local machine.

.. _Docker: https://www.docker.com/
.. _containers: https://en.wikipedia.org/wiki/Container_(virtualization)
.. _Docker Engine: https://docs.docker.com/engine/
.. _Docker Hub: https://hub.docker.com/
.. _Malcolm McLean: https://en.wikipedia.org/wiki/Malcom_McLean
.. _Virtual machine: https://www.vmware.com/topics/virtual-machine
.. _Hypervisor: https://en.wikipedia.org/wiki/Hypervisor
.. _Parallels: https://www.parallels.com/
.. _VirtualBox: https://www.virtualbox.org/
.. _LXC: https://linuxcontainers.org/
.. _OpenVZ: https://openvz.org/
