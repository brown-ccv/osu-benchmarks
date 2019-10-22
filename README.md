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
- Run on all the architectures on Oscar.  I believe you cannot run across archictectures, but we should confirm this

### Todo list:

- Create a module osu-test
- Record how long each benchmark takes
- Format the output of the benchmarks & the node  - what is a sensible way to do this?
- Wrap up the benchmark + formatting + info in a scripting language of your choice.  Output to text file and database.  
- Database - how to ship of the results - we'll need to talk to someone who knows what they are doing with this.
- Cron job to run benchmarks 
