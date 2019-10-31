# osu-benchmarks

Oscar OSU benchmarks

## Aim: 

Run OSU benchmarks on Oscar for openmpi and mvapich2.   

### Questions we are trying to answer:
    Which performs better on Oscar, Openmpi or Mvapich
    How do the bandwith/latency results vary with time and architecture
    Is there any correlation bewteen jobs/users (slurm) and OSU benchmark performance

### How we are approaching this
- Run the benchmarks multiple times per day. (Cron)
- Record:
    - which nodes the benchmarks ran on (hostname, architecture, infiniband)
    - time & date
    - job id
    - benchmark results
    - anything else you can think of
- Run on all the architectures on Oscar.  I believe you cannot run across architecture, but we should confirm this

### Todo list:

- <del>Create a module osu-test</del> done: osu-mpi/5.6.2_mvapich2-2.3a_gcc
- <del>Make a script to track benchmark between which node has been done (recently) and which needs to be done</del> done: using geometric series
- <del>Record how long each benchmark takes</del> done for one bench
- Identify which benchmark functions to use
- Format the output of the benchmarks & the node  - what is a sensible way to do this?
- Wrap up the benchmark + formatting + info in a scripting language of your choice.  Output to text file and database.  
- Database - how to ship of the results - we'll need to talk to someone who knows what they are doing with this.
- Cron job to run benchmarks 
