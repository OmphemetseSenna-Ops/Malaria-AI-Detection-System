from step_001_dataset_merging import run as run_merge
from step_002_dataset_analysis import analyze_dataset as run_analysis


def main():
    print("Starting dataset pipeline")

    # run_merge()
    run_analysis()

    print("Pipeline completed")


if __name__ == "__main__":
    main()