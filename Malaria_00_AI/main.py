from step_001_dataset_merging import run as run_merge
from step_002_dataset_analysis import analyze_dataset as run_analysis
from step_003_class_imbalance_analysis import analyze_class_distribution
from step_003_data_visualization import visualize_distributions
from step_004_data_cleaning import clean_datasets


def main():
    print("Starting dataset pipeline")

    # run_merge()
    # clean_datasets()
    run_analysis()
    analyze_class_distribution()
    visualize_distributions()

    print("Pipeline completed")


if __name__ == "__main__":
    main()