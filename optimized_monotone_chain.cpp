#include<bits/stdc++.h> // This already includes <algorithm> for std::is_sorted
#include<fstream>
#include<string>
using namespace std;

struct pt {
    double x, y;
};

// ... (orientation, cw, ccw functions are UNCHANGED) ...
int orientation(pt a, pt b, pt c) {
    double v = a.x*(b.y-c.y)+b.x*(c.y-a.y)+c.x*(a.y-b.y);
    if (v < 0) return -1; 
    if (v > 0) return +1;
    return 0;
}

bool cw(pt a, pt b, pt c, bool include_collinear) {
    int o = orientation(a, b, c);
    return o < 0 || (include_collinear && o == 0);
}
bool ccw(pt a, pt b, pt c, bool include_collinear) {
    int o = orientation(a, b, c);
    return o > 0 || (include_collinear && o == 0);
}

// --- !!! MODIFIED convex_hull function !!! ---
void convex_hull(vector<pt>& a, bool include_collinear = false) {
    if (a.size() <= 2)
        return;

    // --- 1. Define the comparison lambda once ---
    auto lexicographical_compare = [](pt a, pt b) {
        return make_pair(a.x, a.y) < make_pair(b.x, b.y);
    };

    // --- 2. Add the O(n) check ---
    //    Only sort if the vector is NOT already sorted.
    if (!is_sorted(a.begin(), a.end(), lexicographical_compare)) {
        // --- 3. Run the O(n log n) sort only if needed ---
        sort(a.begin(), a.end(), lexicographical_compare);
    }
    // --- End of optimization ---


    pt p1 = a[0], p2 = a.back();
    vector<pt> up, down;
    up.push_back(p1);
    down.push_back(p1);
    for (int i = 1; i < (int)a.size(); i++) {
        if (i == a.size() - 1 || cw(p1, a[i], p2, include_collinear)) {
            while (up.size() >= 2 && !cw(up[up.size()-2], up[up.size()-1], a[i], include_collinear))
                up.pop_back();
            up.push_back(a[i]);
        }
        if (i == a.size() - 1 || ccw(p1, a[i], p2, include_collinear)) {
            while (down.size() >= 2 && !ccw(down[down.size()-2], down[down.size()-1], a[i], include_collinear))
                down.pop_back();
            down.push_back(a[i]);
        }
    }

    if (include_collinear && up.size() == a.size()) {
        reverse(a.begin(), a.end());
        return;
    }
    a.clear();
    for (int i = 0; i < (int)up.size(); i++)
        a.push_back(up[i]);
    for (int i = down.size() - 2; i > 0; i--)
        a.push_back(down[i]);
}

// --- solve function remains unchanged ---
void solve(vector<pt>& a, ofstream &outfile, int p)
{
    // The vector 'a' already contains all points.
    
    // Process the convex hull
    convex_hull(a, 0); 
    
    // Output the results WITHOUT "CASE 1"
    for(size_t i = 0; i < a.size(); i++)
    {
        // Use fixed and setprecision for double coordinates
        outfile << fixed << setprecision(8) << a[i].x << " " << a[i].y << endl;
    }
}

// --- main function remains unchanged ---
int main(int argc, char* argv[])
{
    // 1. Check for the correct number of command-line arguments
    if (argc != 2) {
        // Print error message to cerr (standard error)
        cerr << "Error: Incorrect usage." << endl;
        // argv[0] is the name of the program itself
        cerr << "Usage: " << argv[0] << " <input_filename.txt>" << endl; 
        return 1; // Return an error code
    }

    // 2. Get the input filename from the command-line argument
    string input_filename = argv[1]; 

    // 3. Construct the output filename
    string output_filename = input_filename;
    size_t dot_pos = output_filename.rfind('.');
    
    if (dot_pos == string::npos) {
        output_filename += "_output.txt";
    } else {
        output_filename.insert(dot_pos, "_output");
    }

    // 4. Open the file streams
    ifstream file(input_filename);
    ofstream outfile(output_filename);

    if (!file.is_open()) {
        cerr << "Error: Could not open input file " << input_filename << endl;
        return 1;
    }
    if (!outfile.is_open()) {
        cerr << "Error: Could not open output file " << output_filename << endl;
        return 1;
    }
    
    // 5. Read ALL points from the file
    vector<pt> all_points;
    double x_val, y_val;
    while (file >> x_val >> y_val) {
        all_points.push_back({x_val, y_val});
    }

    if (all_points.empty()) {
        cerr << "Error: Input file " << input_filename << " contains no valid points." << endl;
        file.close();
        outfile.close();
        return 1;
    }

    // 6. Run the solve function once
    cout << "Processing " << all_points.size() << " points from " << input_filename << "..." << endl;
    // We pass 1 for 'p' but the solve function no longer uses it.
    solve(all_points, outfile, 1); 

    // 7. Close files and exit
    file.close();
    outfile.close();
    cout << "Processing complete! Results saved to: " << output_filename << endl;
    
    return 0;
}