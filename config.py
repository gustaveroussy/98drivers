
# Features 
features = [
	"features/exons.bed",
	"features/introns.bed"
]

genome_sizes = "features/genome.size"

output = "output/"

# # To render html link 
# igv_port   = 60151
# igv_host   = "localhost"

# Cluster detection 
## maximum distance between mutation allowed to be merge.
c_distance       = 500 
c_count          = 50 
c_distinct_count = 50

# Peaks detections 
## The maximuim width of peaks 
p_width = 5
## How many mutation occurs in the peaks 
p_count = 5
## How many uniq patient mutation occurs in the peaks 
p_distinct_count = 5

# Size of range to compute Mutation count. NbMutation per X 
mutation_range = 1000000