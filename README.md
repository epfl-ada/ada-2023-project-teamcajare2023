# Studying the evolution of gender in movies across the world: roles given to women and public perception

## Abstract

Women face an array of stereotypes, from traditional domestic roles to uncertainties surrounding their capacity for leadership, physical strength, and the added pressure of conforming to beauty standards. The film industry, often seen as reflecting our societal norms, perpetuates these stereotypes. Our objective is to explore this phenomenon and pinpoint the areas where these biases are most outstanding.

Moreover, we aim to enrich our analysis with a regional dimension. Stereotypes exist regarding major movie industries around the world: Hollywood often leans toward blockbuster entertainment, possibly emphasizing masculinity, whereas European productions are often perceived as more artistic, intellectual, and potentially more gender-equitable. Bollywood movies tend to have family-centric plots, influencing the roles designated to actresses.

To decipher and validate or debunk these common perceptions, our analysis will begin by studying the evolving roles allocated to women in movies. Then, we will juxtapose these findings across different movie industries.

## Research questions

Knowing that women are treated differently in the movie industry, we are interested to dig deeper:
- Explore quantitatively the extend of the inequalities in the representation of women: How younger are the actresses compared to the actors? What is the difference in the proportion of actresses and actors? What genres are more prone to inequalities?
- Explore qualitatively how women are represented in the movies through the character types of female and male roles: what are the typical roles? How have they evolved?
- Understand how movies with higher proportions of women are received by the public: are those movies more or less popular? How are they rated? Do they have less commercial success than movies with more men?
- Analyse those differences around three geographical areas we have chosen (USA, India and Europe): are the preconceived ideas about Hollywood, Bollywood and European movie industries true when it comes to the roles of women in the plot? 

## Proposed additional datasets 

**IMDb ratings**: IMDb is an [online database](https://datasets.imdbws.com/) of information related to films, television series and more, where users can rate the films they watch from 1 to 10. We are mainly interested in the IMDb average score and number of votes per movie (title.ratings.tsv and title.basics.tsv).

**Oscar awards**: Awards are international recognition of excellence in cinema. Using this [kaggle dataset](https://www.kaggle.com/datasets/unanimad/the-oscar-award) we got the list of films that were awarded by the Academy Awards.

**Bechdel Test**: The Bechdel test is a measure of the representation of women in film. We used the [Bechdel Kaggle dataset](https://www.kaggle.com/datasets/treelunar/bechdel-test-movies-as-of-feb-28-2023) to obtain the test results for several thousands of film.

## Methods

## Step 1: Data scrapping and cleaning 
After having downloaded the characters and movies metadata as well as IMDb data, we clean the datasets by removing movies where we have no information about characters' gender and discarding aberrant age, movie runtime or release date values.

## Step 2: Data pre-processing
We merge the movies and characters datasets. In it, we keep only the 16 more frequent movie genres
DECRIRE PLUS

## Step 2: Analysis

### Part 1 : Quantitative analysis of gender inequalities in movies
- Age of actors and actresses and Gender distribution in characters: Analysis of distributions and of the statistical significance (t-test), Evolution across the years with confidence interval
- Analysis across genre of movie of age and gender distribution
- Analysis of number of movies shot per actor and actress

### Part 2 : Qualititative analysis of gender representation in movies
- Word Cloud visualization of common character tropes per gender
- Cluster character types from the movie plots: the authors of the dataset used the CoreNLP toolkit developed by Stanford University to parse the movie plot summaries. Extract meaningful information about the characters: what action they are the agent or patient of, what their attributes are, how many times they are mentioned in the summary (proxy to identify the main character). With all of those information, we will cluster the characters to identify similar ones and then perform further analysis of those cluster (gender, longitudinal and geographical differences).

### Part 3 : Analysis of the reception of movies by the public
- Analysis of the correlation of actresses in a movie and IMDb ratings with a linear regression, calculate statistical significance (same with Box Office Revenue)
- Analysis of award wining movies with the oscar dataset
- Analysis of the Bechdel test result in relation with the reception of the movie

### Part 4 : Analysis by geographical production region
- Analysis of the character cluster per production region
- Quantification of gender differences across the regions

## Proposed timeline

- 24 Nov : Finish quantitative analysis and the reception of movies
- 1 Dec : Finish analysis by geographical production region
- 8 Dec : Finish qualitative analysis of gender representation and make first version of the website
- 15 Dec : Finish all the analysis and focus on completing the data story and the aesthetics of the website
- 22 Dec : Final deadline for P3

## Organization within the team
| | Task |
| :---:|---|
| Amélie | Preprocessing of movie data set, Preprocessing of geographical regions|
| Anna-Rose | Cluster character types from the movie plots|
| Coline | Preprocessing of the character data set and IMDb, Age analysis|
| Elisa | Analysis of Box-office revenue and ratings, Preprocessing of awards |
| Jeanne | Preprocessing of Bechdel test, Geographical analysis |

## Questions
- Bechdel data set: when merging with the CMU dataset, we are left with around 5000 movies (only 6.17 % of the original). Can we consider this data set usable?