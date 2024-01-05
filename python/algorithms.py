from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from plotting import *

"""
These Functions Were Created When Identifying The Process Required To Get To The Final 3 Functions At The End Of This 
File.

Basically It Provides A ... Workflow And Reiteration Process For The K-Means and PCA Methods For Helping To Identify 
Which Segments Are Attributed To Which Variables
"""


def k_means_data(dataframe=None, cats: int = 5):
    """
    This Function Takes The Inputs And Returns The Labels Created By The KMeans Method.
    """
    if dataframe is None:
        return ValueError("A dataframe must be populated as the first argument.")
    kmeans = KMeans(n_clusters=cats)
    kmeans.fit(dataframe)
    labels = kmeans.labels_
    return labels


def update_means_and_data(std_data, raw_data, mapper):
    """
    This Function Is Just A Data Cleaner That Was Needed At One Point In The Development Process. I Needed To Clean The
    Notebook From Distractions
    """
    std_data["Segment"] = std_data["Segment"].astype("int64")
    std_data["Label"] = std_data["Segment"].replace(mapper)
    raw_data["Segment"] = raw_data["Segment"].astype("int64")
    raw_data["Label"] = raw_data["Segment"].replace(mapper)
    return std_data, raw_data


def get_pca(DF, num_components=None):
    """ Simple Function Which Returns A Pre-fit PCA Object """
    if num_components is None:
        pca = PCA()
    else:
        pca = PCA(n_components=num_components)
    pca.fit(DF)
    return pca


def get_scaled_data(DF):
    """
    Scales The DataFrame Data Provided And Transforms It Since This Isn't A Machine Learning Assignment Per se
    Otherwise It Would Need To Be Transformed After Training.
    """
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(DF)
    scaled_data = pd.DataFrame(scaled_data, columns=DF.columns)
    return scaled_data


def get_component_df(df_with_cols, pca_pointer, component_names):
    """
    Creates The Component Df Which Is Just The DataFrame In The Project Which Is Used For Helping In Seeing The
    Segments Given TO Variables. The Components Are Just Fill Ins For The Variables Which Are Hitherto Not Defined
    """
    return pd.DataFrame(data=pca_pointer.components_, columns=df_with_cols.columns, index=component_names)


def segment1(DF, perk_map, num_clusters):
    """
    The Segment Function Scales and Segments The Data For Running Further Tests. The Outputs Are DataFrames In
    Different Configurations or Modifications Of The Data Depending On The Requirement Of Whichever The Next Function Is
    """
    raw_unscaled_data = DF.copy()

    #     GET THE SCALED DATA USING SCALER
    raw_scaled_data = get_scaled_data(raw_unscaled_data)

    #     RUN THE K-MEANS ALGORITHM
    kmeans = KMeans(n_clusters=num_clusters, random_state=0, n_init='auto')
    kmeans.fit(raw_scaled_data)

    #     COPY ORIGINAL DATA FOR USE LATER
    unscaled_segmented_data = raw_unscaled_data.copy()
    scaled_segmented_data = raw_scaled_data.copy()

    #     ADD THE K-MEANS LABELS FOR FURTHER PROCESSING
    unscaled_segmented_data["Segment"] = kmeans.labels_
    scaled_segmented_data["Segment"] = kmeans.labels_

    #     CREATE NEW DFs FOR GETTING THE AVERAGES OF ACCUMULATED DATA THUS FAR TO DETERMINE WHAT LABELS TO APPLY TO EACH
    unscaled_data_means = unscaled_segmented_data.groupby(["Segment"]).mean()
    scaled_data_means = scaled_segmented_data.groupby(["Segment"]).mean()

    #     REPLACE THE INDEX OF THE AGGREGATED DATA TO BE THE PERKS INSTEAD
    scaled_data_means = scaled_data_means.replace(perk_map)

    #     CREATE THE LABEL COLUMN TO ASSOCIATE PERKS AND LABELS RECEIVED
    unscaled_segmented_data["Segment"] = unscaled_segmented_data["Segment"].astype("int64")
    unscaled_segmented_data["Label"] = unscaled_segmented_data["Segment"].replace(perk_map)

    scaled_segmented_data["Segment"] = scaled_segmented_data["Segment"].astype("int64")
    scaled_segmented_data["Label"] = scaled_segmented_data["Segment"].replace(perk_map)

    #     RETURN DATA FOR USE IN FURTHER ITERATIONS
    return (
        raw_unscaled_data,
        raw_scaled_data,
        unscaled_segmented_data,
        scaled_segmented_data,
        unscaled_data_means,
        scaled_data_means
    )


def scale2(raw_scaled_data, starting_data, scaled_segmented_data, x_col, y_col, run_plots=False):
    """
    The scale2 Function Is The Second Function In The Basic Workflow Which Provides The pca For Observation Of The
    Results And The component_df Which Is A DataFrame With Compoent Identifier For Viewing And Making Determinations In
    Terms Of Which Variables Are Statistically Useful To Include In The Final Algorithm.
    """

    pca = get_pca(raw_scaled_data)

    num_components = len(starting_data.columns)
    components = [f"Component {x + 1}" for x in range(num_components)]
    component_df = get_component_df(starting_data, pca, components)

    if run_plots:
        variance_chart(pca)
        compare_hmap(component_df, components)
        seg_plot(scaled_segmented_data, x_col, y_col)

    return pca, component_df


def compare3(DF, perk_map, run_plots, num_clusters=5):
    """
    The compare3 Function Is Used For Final Analysis And Provides The Final Output For Use In Final Viewing Of The
    Clusters As Well As The Other Data Needed. These Functions Are Just A More Clean Way Of Running The Workflow And
    Keeping Distractions Away This Is The Iterative Aspect Of The Workflow.
    """
    starting_data2 = DF.copy()

    raw_unscaled_data2, \
        raw_scaled_data2, \
        unscaled_segmented_data2, \
        scaled_segmented_data2, \
        unscaled_data_means2, \
        scaled_data_means2 = segment1(
        starting_data2,
        perk_map,
        num_clusters)

    num_components2 = 5
    pca2 = get_pca(raw_scaled_data2, num_components2)

    components2 = [f"Component {x + 1}" for x in range(num_components2)]
    component_df2 = get_component_df(starting_data2, pca2, components2)

    if run_plots:
        variance_chart(pca2)
        compare_hmap(component_df2, components2)

    return pca2, components2, component_df2, segment1(
        starting_data2,
        perk_map,
        num_clusters)
