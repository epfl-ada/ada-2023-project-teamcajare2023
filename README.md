# Studying the evolution of gender in movies: roles given to women and public perception

## Abstract

Women face an array of stereotypes, from traditional domestic roles to uncertainties surrounding their capacity for leadership, physical strength, and the added pressure of conforming to beauty standards. The film industry, often seen as reflecting our societal norms, perpetuates these stereotypes. Our objective is to explore this phenomenon and pinpoint the areas where these biases are most outstanding.

Moreover, we aim to enrich our analysis with a regional dimension. Stereotypes exist regarding major movie industries around the world: American cinema often leans toward blockbuster entertainment, possibly emphasizing masculinity, whereas European productions are often perceived as more artistic, intellectual, and potentially more gender-equitable. Bollywood movies tend to have family-centric plots, influencing the roles designated to actresses.

To decipher and validate or debunk these common perceptions, our analysis will begin by studying the evolving roles allocated to women in movies. Subsequently, we will juxtapose these findings across different movie industries.

## Research questions

Knowing that women are treated differently in the movie industry, we are interested to dig deeper:
- Explore quantitatively the extend of the inequalities in the representation of women in movies: How younger are the actresses compared to the actors? What is the difference in the proportion of actresses and actors? What genres are more prone to inequalities?
- Explore qualitatively how women are represented in the movies through the character types of female and male roles: what are the typical roles? How have they evolved?
- Understand how movies with higher proportions of women are recieved by the public: are those movies more or less popular? How are they rated? Do they really have less commercial success than movies with more men?
- Analyse those differences around three geographical zones we have chosen (North America, Europe, India): are the preconceived ideas about Hollywood, Bollywood and European movie industries true when it comes to the roles of women in the plot? 

## Proposed additional datasets 

**IMDb ratings**: IMDb (an acronym for Internet Movie Database) is an [online database](https://datasets.imdbws.com/) of information related to films, television series and more, where users can rate the films they watch from 1 to 10. We are mainly interested in the IMDb average score and number of votes per movie. The IMDb title basics and title ratings datasets have been found on IMDb (title.ratings.tsv and title.basics.tsv). 

**Oscar awards**: From a [kaggle dataset](https://www.kaggle.com/datasets/unanimad/the-oscar-award) we use the list of films that were awared by the Academy Awards. These awards are an international recognition of excellence in cinematic achievements. The various category winners are awarded a copy of a golden statuette, commonly referred to by its nickname "Oscar".

**Bechdel Test**: JEANNE DESCRIPTION

## Methods

## Step 1: Data scrapping and cleaning 
After having downloaded the characters and movies metadata as well as IMDb data, we clean the datasets by removing movies where we have no information about characters' gender and discarding aberrant age, movie runtime or release date values.

## Step 2: Data pre-processing
We merge the movies and characters datasets. In it, we keep only the 16 more frequent movie genres
DECRIRE PLUS

## Step 3: Analysis

### Part 1 : Quantitative analysis of gender inequalities in movies
- Age of actors and actresses : Analysis of distributions and of the statistical significance (t-test), Evolution across the years with confidence interval
- Gender distribution in charcters: quantification and analysis across the years with confidence interval
- Analysis across genre of movie of age and gender distribution
- Analysis of number of movies shot per actor and actress

### Part 2 : Qualititative analysis of gender representation in movies
- Word Cloud visualization of common character tropes per gender
- Cluster character types from the movie plots ( ANNA-ROSE DESCRIPTION)

### Part 3 : Analysis of the reception of movies by the public
- Analysis of the correlation of actresses in a movie and IMDb ratings with a linear regression, calculate statistical significance
- Analysis of the correlation of actresses in a movie and Bos Office Revenue with a linear regression, calculate statistical significance
- Analysis of award wining movies with the oscar dataset
- According to the Bechdel test result analysis of the reception of the movie

### Part 4 : Analysis by geographical production region
- Analysis of the character cluster per production region
- Quantification of gender differences across the regions


## Proposed timeline

- 24 Nov : Finish quantitative analysis of gender inequalities and of the reception of movies by the public
- 1 Dec : Finish analysis by geographical production region
- 8 Dec : Finish qualititative analysis of gender representation in movies and make first version of the website
- 15 Dec : Finish all the analysis and focus on completing the data story and the esthetics of the website
- 22 Dec : Final deadline for P3

## Organization within the team
| | Task |
| :---:|---|
| Amélie | |
| Anna-Rose | |
| Coline | |
| Elisa | Analysis of Box office revenue and ratings, README |
| Jeanne | |
## Questions
