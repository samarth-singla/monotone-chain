#include<bits/stdc++.h>
#include<fstream>
#include<string>
using namespace std;

struct pt {
    double x, y;
};

// ... (orientation, cw, ccw, convex_hull functions remain unchanged) ...
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

void convex_hull(vector<pt>& a, bool include_collinear = false) {
    if (a.size() <= 2)
        return;

    sort(a.begin(), a.end(), [](pt a, pt b) {
        return make_pair(a.x, a.y) < make_pair(b.x, b.y);
    });
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

// --- MODIFIED solve function ---
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
int main()
{
    // 1. Prompt the user for the input filename
    cout << "Enter the input filename (e.g., points.txt): ";
    string input_filename;
    cin >> input_filename; 

    // 2. Construct the output filename
    string output_filename = input_filename;
    size_t dot_pos = output_filename.rfind('.');
    
    if (dot_pos == string::npos) {
        output_filename += "_output.txt";
    } else {
        output_filename.insert(dot_pos, "_output");
    }

    // 3. Open the file streams
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
    
    // 4. Read ALL points from the file
    vector<pt> all_points;
    double x_val, y_val;
    while (file >> x_val >> y_val) {
        all_points.push_back({x_val, y_val});
    }

    if (all_points.empty()) {
        cerr << "Error: Input file " << input_filename << " contains no valid points." << endl;
        return 1;
    }

    // 5. Run the solve function once
    cout << "Processing " << all_points.size() << " points..." << endl;
    // We pass 1 for 'p' but the solve function no longer uses it for output.
    solve(all_points, outfile, 1); 

    // 6. Close files and exit
    file.close();
    outfile.close();
    cout << "Processing complete! Results saved to: " << output_filename << endl;
    
    return 0;
}


//BASE CASE->all sorted points
//