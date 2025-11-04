rule all:
    input:
        "outputs/ve_by_week.png"

rule synth:
    output: "outputs/synth.csv"
    shell:
        "python scripts/generate_synth.py --n 5000 --weeks 12 --sites 5 --seed 42 --out {output}"

rule estimate:
    input: "outputs/synth.csv"
    output: "outputs/ve_by_week.csv"
    shell:
        "python scripts/estimate_ve.py --data {input} --serology-se 0.92 --serology-sp 0.98 --n-imputations 50 --sample-se-sp --by week --out {output}"

rule plot:
    input: "outputs/ve_by_week.csv"
    output: "outputs/ve_by_week.png"
    shell:
        "python scripts/plot_ve.py --ve {input} --out {output}"
