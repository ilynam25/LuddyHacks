export const chooseDegreeOffInterests = async (interests) => {
    let degreeToInterests = {};
    let interestToDegrees = {};
    const response = await fetch('/explore_programs_majors_raw.txt');
    const fileContent = await response.text();
    console.log(fileContent);
    const lines = fileContent.trim().split('\n');
    degreeToInterests = {};
    interestToDegrees = {};
  
    for (let i = 0; i < lines.length; i += 2) {
      const degree = lines[i].trim();
      const parsedInterests = lines[i + 1]
        .split('#')
        .filter(Boolean)
        .map(s => s.trim());
  
      degreeToInterests[degree] = parsedInterests;
  
      for (const interest of parsedInterests) {
        if (!interestToDegrees[interest]) {
          interestToDegrees[interest] = [];
        }
        interestToDegrees[interest].push(degree);
      }
    }
  
    const degreeCounts = {};
    const degreesWithInterest = {};
  
    for (const interest of interests) {
      if (interestToDegrees[interest]) {
        interestToDegrees[interest].forEach(degree => {
          if (!degreeCounts[degree]) {
            degreeCounts[degree] = 1;
            degreesWithInterest[degree] = [interest];
          } else {
            degreeCounts[degree]++;
            degreesWithInterest[degree].push(interest);
          }
        });
      }
    }
  
    return Object.entries(degreeCounts)
      .sort((a, b) => b[1] - a[1])
      .slice(0, 3)
      .map(([degree]) => ({
        degree,
        matchingInterests: degreesWithInterest[degree],
      }));
  };
  