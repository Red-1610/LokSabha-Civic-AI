import csv
import random
import os

def generate_election_data():
    states = ["West Bengal", "Maharashtra", "Uttar Pradesh", "Tamil Nadu", "Karnataka", "Gujarat", "Rajasthan", "Kerala"]
    parties = ["Party A", "Party B", "Party C", "Independent"]
    
    filename = "historical_election_data.csv"
    target_size_mb = 5.5
    target_bytes = target_size_mb * 1024 * 1024
    
    print(f"Generating {target_size_mb} MB of historical election data...")
    
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Year", "State", "Constituency", "Party", "Votes", "Voter_Turnout_Percentage"])
        
        row_count = 0
        while os.path.getsize(filename) < target_bytes:
            year = random.choice(range(1950, 2024, 4))
            state = random.choice(states)
            constituency = f"Constituency_{random.randint(1, 500)}"
            party = random.choice(parties)
            votes = random.randint(10000, 500000)
            turnout = round(random.uniform(45.0, 85.0), 2)
            
            writer.writerow([year, state, constituency, party, votes, turnout])
            row_count += 1
            
            # Flush occasionally to check accurate size
            if row_count % 10000 == 0:
                file.flush()

    print(f"Success! Generated {row_count} records. File size is now ~{target_size_mb} MB.")

if __name__ == "__main__":
    generate_election_data()
