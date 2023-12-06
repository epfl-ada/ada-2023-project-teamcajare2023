# Studying the evolution of gender in movies across the world: roles given to women and public perception

## Abstract

Our aim is to examine the extent to which the film industry, as a mirror of societal norms, perpetuates stereotypes about women, whether in terms of domestic roles, leadership doubts or standards of beauty. We will also explore regional variations: American cinema's emphasis on masculinity in blockbusters, the artistic and intellectual nature of European films, with perhaps greater gender equity, and Bollywood's family-centric themes, which affect the roles of female actors. Our analysis begins with the changing roles of women in films, and then compares them across different film industries.

## Research questions

Knowing that women are treated differently in the movie industry, we are interested to dig deeper:
- Explore quantitatively the extent of the inequalities in the representation of women: How younger are the actresses compared to the actors? What is the difference in the proportion of actresses and actors? What genres are more prone to inequalities?
- Explore qualitatively how women are represented in the movies through the character types of female and male roles: what are the typical roles? How have they evolved?
- Understand how movies with higher proportions of women are received by the public: are those movies more or less popular? How are they rated? Do they have less commercial success than movies with more men?
- Analyze those differences around three geographical areas we have chosen (USA, India and Europe): are the preconceived ideas about Hollywood, Bollywood and European movie industries true when it comes to the roles of women in the plot? 

## Proposed additional datasets 

**IMDb ratings**: IMDb is an [online database](https://datasets.imdbws.com/) of information related to films, television series and more, where users can rate the films they watch from 1 to 10. We are mainly interested in the IMDb average score and number of votes per movie (title.ratings.tsv and title.basics.tsv).

**Oscar awards**: Awards are international recognition of excellence in cinema. Using this [kaggle dataset](https://www.kaggle.com/datasets/unanimad/the-oscar-award) we got the list of films that were awarded by the Academy Awards.

**Bechdel Test**: The Bechdel test is a measure of the representation of women in film. We used the [Bechdel Kaggle dataset](https://www.kaggle.com/datasets/treelunar/bechdel-test-movies-as-of-feb-28-2023) to obtain the test results. We have a rating where 1 means a movie has two female characters but they do not talk to each other, 2 means a movie has two women talking but they talk about men and 3 means completely passing the Bechdel Test.

## Methods

## Step 1: Data cleaning and pre-processing
- **CMU Dataset**
  - We cleaned the dataset by discarding rows with aberrant age, movie runtime or release date values.
  - We deleted the rows for which we had no information on gender.
  - We conducted an inner join between the movies and characters datasets to include only movies with characters in our analysis, thereby populating the characters dataset.
  - We filtered the dataset to include only movies from 1925 to 2012, ensuring a minimum of 200 movies and 100 characters per year.
  - We standardized country names using the pycountry library's ISO databases and added continent information. Rows with multiple different continents were removed.

- **IMDb Dataset**
  - The IMDb dataset comprises two files—one with ratings and another with various movie names. We calculated the average ratings for each movie.
  - We merged the IMDb dataset with the CMU dataset using the (english) movie name and release year as the merging criteria.

- **Bechdel Dataset** We changed the movie names to align with the CMU format and then merged them based on the movie name and release year.

- **Award Dataset** We merged the award dataset with the CMU dataset based on movie name and release year.


## Step 2: Analysis

### Part 1 : Quantitative analysis of gender inequalities in movies
- Age of actors and actresses and Gender distribution in characters: Analysis of distributions and of the statistical significance (t-test), Evolution across the years with confidence interval
- Analysis across genre of movie of age and gender distribution
- Analysis of number of movies shot per actor and actress

### Part 2 : Qualitative analysis of gender representation in movies
- Word Cloud visualization of common character tropes per gender
- Cluster character types from the movie plots: the authors of the dataset used the CoreNLP toolkit developed by Stanford University to parse the movie plot summaries. Extract meaningful information about the characters: what action they are the agent or patient of, what their attributes are, how many times they are mentioned in the summary (proxy to identify the main character). With all of those information, we will cluster the characters to identify similar ones and then perform further analysis of those cluster (gender, longitudinal and geographical differences).

### Part 3 : Analysis of the reception of movies by the public
- Analysis of the correlation of actresses in a movie and IMDb ratings with a linear regression, calculate statistical significance (same with Box Office Revenue)
- Analysis of award wining movies with the oscar dataset
- Analysis of the Bechdel test result in relation with the reception of the movie

### Part 4 : Analysis by geographical production region
- Analysis of the character cluster per production region
- Quantification of gender differences across the regions

## Proposed timeline ⏱️

- 24 Nov: Finish quantitative analysis and the reception of movies
- 1 Dec: Finish analysis by geographical production region
- 8 Dec: Finish qualitative analysis of gender representation and make first version of the website
- 15 Dec: Finish all the analysis and focus on completing the data story and the aesthetics of the website
- 22 Dec: Final deadline for P3

## Organization within the team 📋
| | Task |
| :---:|---|
| Amélie | Preprocessing of movie data set, Preprocessing of geographical regions|
| Anna-Rose | Cluster character types from the movie plots|
| Coline | Preprocessing of the character data set and IMDb, Age analysis|
| Elisa | Analysis of Box-office revenue and ratings, Preprocessing of awards |
| Jeanne | Preprocessing of Bechdel test, Geographical analysis |

## Questions 
- Bechdel data set: when merging with the CMU dataset, we are left with around 5000 movies (only 6.17 % of the original). Can we consider this data set usable?
