def choose_degree_of_interests(major_or_minor, interests):
    degree_to_interests = {}
    interest_to_degrees = {}

    # Read the file synchronously
    with open('../explore_programs/explore_programs_' + major_or_minor + '_raw.txt', 'r') as file:
        lines = file.read().strip().split('\n')

    for i in range(0, len(lines), 2):
        degree = lines[i].strip()
        parsed_interests = [s.strip() for s in lines[i + 1].split('#') if s.strip()]

        degree_to_interests[degree] = parsed_interests

        for interest in parsed_interests:
            interest_to_degrees.setdefault(interest, []).append(degree)

    degree_counts = {}
    degrees_with_interest = {}

    for interest in interests:
        for degree in interest_to_degrees.get(interest, []):
            degree_counts[degree] = degree_counts.get(degree, 0) + 1
            degrees_with_interest.setdefault(degree, []).append(interest)

    top_degrees = sorted(degree_counts.items(), key=lambda x: x[1], reverse=True)[:3]

    return [
        {
            'degree': degree,
            'matchingInterests': degrees_with_interest[degree]
        }
        for degree, _ in top_degrees
    ]

# Example usage:
# result = choose_degree_of_interests(['technology', 'business', 'design'])
# print(result)
