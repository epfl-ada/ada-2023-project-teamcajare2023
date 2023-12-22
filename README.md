# Unraveling Gender Stereotypes Across Movie Industries
___Are our preconceived ideas on gender inequality true?___

Look at our [datastory](https://elisabillard.github.io) first !

## Abstract

Our aim is to examine the extent to which the film industry, as a mirror of societal norms, perpetuates stereotypes about women, whether in terms of domestic roles, leadership doubts or standards of beauty. We will also explore regional variations: American cinema's emphasis on masculinity in blockbusters, the artistic and intellectual nature of European films, with perhaps greater gender equity, and Bollywood's family-centric themes, which affect the roles of female actors. Our analysis begins with the changing roles of women in films, and then compares them across different film industries.

## Research questions

Knowing that women are treated differently in the movie industry, we are interested to dig deeper:
- Explore quantitatively the extent of the inequalities in the representation of women: How younger are the actresses compared to the actors? What is the difference in the proportion of actresses and actors? What genres are more prone to inequalities?
- Explore qualitatively how women are represented in the movies through the character types of female and male roles: what are the typical roles? 
- Understand how movies with higher proportions of women and feminine main characters are received by the public: are those movies more or less popular? How are they rated? Do they have less commercial success than movies with more men?
- Analyze those differences around three geographical areas we have chosen (USA, India and Europe): are the preconceived ideas about Hollywood, Bollywood and European movie industries true when it comes to the representation of women in the plot? 

## Proposed additional datasets 

**The Movies dataset**: The main character often serves as the narrative anchor, around whom the story revolves. They are typically central to the plot, driving the storyline forward and engaging the audience's interest and emotions. In our pursuit to understand the significance of the main character's gender, we used this [kaggle dataset](https://www.kaggle.com/datasets/rounakbanik/the-movies-dataset) containing informations about the cast of a movie to retrieve its main character and its associated gender.

**IMDb ratings**: IMDb is an [online database](https://datasets.imdbws.com/) of information related to films, television series and more, where users can rate the films they watch from 1 to 10. We are mainly interested in the IMDb average score and number of votes per movie (title.ratings.tsv and title.basics.tsv).

**Oscar awards**: Awards are international recognition of excellence in cinema. Using this [kaggle dataset](https://www.kaggle.com/datasets/unanimad/the-oscar-award) we got the list of films that were awarded by the Academy Awards.


## Methods

## Step 1: Data cleaning and pre-processing
- **CMU Dataset**
  - We cleaned the dataset by discarding rows with aberrant age, movie runtime or release date values.
  - We deleted the rows for which we had no information on gender or movie genre.
  - We conducted an inner join between the movies and characters datasets to include only movies with characters in our analysis, thereby populating the characters dataset.
  - We filtered the dataset to include only movies from 1925 to 2012, ensuring a minimum of 200 movies and 100 characters per year.
  - We standardized country names using the pycountry library's ISO databases and added continent information. Rows with multiple different continents were removed.
  - We calculated the proportion of female characters in each movie.
  - We calculated the sentiment of each movie plot summary using spacytextblob.

- **The Movies Dataset**
  - We identified, for each movie of the dataset, the main character, the actor who interpreted it and its gender.
  - We deleted the rows for which we had no information on gender.

- **IMDb Dataset**
  - The IMDb dataset comprises two files—one with ratings and another with various movie names. We calculated the average ratings for each movie.
  - We merged the IMDb dataset with the CMU dataset using the (english) movie name and release year as the merging criteria.

- **Award Dataset** We merged the award dataset with the CMU dataset based on movie name and release year.


## Step 2: Analysis

### Part 1 : Quantitative analysis of gender inequalities in movies

#### Age of actors and actresses and gender distribution in characters
- Analysis of distributions and of the statistical significance (t-test), Evolution across the years with confidence interval
- Analysis across genre of movie of age and gender distribution.

#### Sentiment analysis
- *Objective*: Perform causal analysis on the impact of female character percentage and main character gender on film sentiment.
- *Methodology*: Use exact matching based on 5-year bin release periods, movie genre and production country.
- *Analysis*: Employ linear regression to predict film sentiment. 
  - Use separately:
    - Female character percentage.
    - Main character gender.


### Part 2 : Qualitative analysis of gender representation in movies

#### Common character types finding
- Word Cloud visualization of common character tropes per gender.

#### Cluster character types from the movie plots

- *Objective*: Identify patterns and associations between linguistic elements for character type classification.
- *Method*:
  - Using the CoreNLP parsed movie summaries provided by the authors of the dataset, extract agent verbs, patient verbs and attributes describing all characters.
  - Create representations of the characters using word vectors weighted by their inverse document frequency (IDF).
  - Cluster these representations by first reducing dimensionality and then performing K-means.
- *Analysis*:
  - Study percentage of female characters in the obtained clusters.
  - Qualitative characterization of clusters that are significantly gendered using wordclouds.

#### Predict a character's gender based on its linguistic features
- *Objective*: Identify patterns and associations between linguistic elements and gender for character classification.
- *Method*: Develop a neural network classifier to predict the character's gender.
- *Input Features*:
  - Attributes word vectors.
  - Agent verbs word vectors.
  - Patient verbs word vectors.


### Part 3 : Analysis of the reception of movies by the public & cinema industry

#### Public reception: Influence of the percentage of actresses in a movie on IMDb ratings & Box-Office revenue
- Linear Regression with the percentage of actresses to predict the IMDb ratings or the Box Office Revenue.

- Causal examination of the impact of female character percentage and main character gender on IMDb ratings.
  
  - *Methodology*: Exact matching based on 5-year bins for release year periods, movie genre and production country.
  - *Analysis*:
    - Employ linear regression models to predict IMDb ratings:
        - Using the percentage of female characters.
        - Using the main character's gender.
    - Machine Learning Regressor Analysis:
      - Evaluate mean-squared error between two GradientBoostingRegression models: one includes the percentage of female characters (or main character's gender); the other excludes it.

#### Industry reception: Influence of the main character's gender on award nomination
- Causal analysis of the impact of the main character's gender on the likelihood of receiving award nominations.
  - *Methodology*:  exact matching on the release year period, the movie genre and the production country
  - *Analysis*: Logit regression to predict the likelihood of being nominated for an award based on the main character's gender.


### Part 4 : Analysis by geographical production region
- **TO CHECK** Qualitative analysis of the character cluster per production region.

- Causal analysis of the differences of percentage of female characters in movies produced in Europe, India and the USA.
  - *Methodology*: exact matching (triplet of movies) on the release year period (5-year bins) and movie genre.
  - *Analysis*: ANOVA to assess the signifiance of the difference and Tukey's test to find in which group the difference is significant.


## Executed timeline ⏱️

- 10 Dec: Finish the reception of movies analysis
- 11 Dec: Finish the gender classifier
- 15 Dec: Finish analysis by geographical production region
- 18 Dec: Finish sentiment analysis
- 20 Dec: Finish all the analysis and focus on completing the data story and the aesthetics of the website
- 22 Dec: Final deadline for P3

## Organization within the team 📋
| | Task |
| :---:|---|
| Amélie | Preprocessing of movie data set, preprocessing of geographical regions, award nomination analysis, data story writing, building of the data story's website |
| Anna-Rose | Preprocessing of the CoreNLP dataset, cluster character types from the movie plots, building of the gender classifier |
| Coline | Preprocessing of the character data set and IMDb, age analysis, Sentiment analysis, geographical analysis, analysis of rating |
| Elisa | Analysis of Box-office revenue and ratings, preprocessing of the awards dataset, geographical matching, data story writing, building of the data story's website |
| Jeanne | Geographical analysis, |
