// new guides from the editorial queue
COPY Guide FROM 'staging/guides.csv' (header=true);
COPY ABOUT FROM 'staging/about.csv' (header=true);
COPY AVAILABLE_IN FROM 'staging/available_in.csv' (header=true);
COPY WROTE FROM 'staging/wrote.csv' (header=true);
