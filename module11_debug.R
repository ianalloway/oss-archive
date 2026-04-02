# ============================================================
# Module 11 – Debugging & Defensive Programming in R
# LIS 4805 – Ian Alloway
# ============================================================

# ---- helper: Tukey outlier rule for a single vector --------
tukey.outlier <- function(v) {
    qq  <- quantile(v, c(0.25, 0.75))
    iqr <- IQR(v)
    (v < qq[1] - 1.5 * iqr) | (v > qq[2] + 1.5 * iqr)
  }

# ---- Task 1: Reproduce the error ----------------------------
# Original (buggy) function
tukey_multiple_buggy <- function(x) {
    outliers <- array(TRUE, dim = dim(x))
    for (j in 1:ncol(x)) {
          outliers[, j] <- outliers[, j] && tukey.outlier(x[, j])
        }
    outlier.vec <- vector("logical", length = nrow(x))
    for (i in 1:nrow(x)) {
          outlier.vec[i] <- all(outliers[i, ])
        }
    return(outlier.vec)
  }

set.seed(123)
test_mat <- matrix(rnorm(50), nrow = 10)

cat("=== Task 1: Reproduce the Error ===\n")
result_buggy <- tryCatch(
    tukey_multiple_buggy(test_mat),
    warning = function(w) {
          cat("WARNING:", conditionMessage(w), "\n")
          invokeRestart("muffleWarning")
        },
    error = function(e) {
          cat("ERROR:", conditionMessage(e), "\n")
          NULL
        }
  )
# Expected warning:
# "the condition has length > 1 and only the first element will be used"

# ---- Task 2: Diagnose the Bug --------------------------------
# The operator && is a SCALAR logical AND — it evaluates only
# the first element of each side and returns a single TRUE/FALSE.
# Inside the loop we need an ELEMENT-WISE logical AND (&) so
# that every row of the column is compared independently.
# Using && collapses the entire column comparison to one value,
# which triggers the warning and produces wrong results.

# ---- Task 3: Fix the Code ------------------------------------
cat("\n=== Task 3 & 4: Corrected Function ===\n")

corrected_tukey <- function(x) {
    # ---- Task 5: Defensive checks ----
    if (!is.matrix(x)) {
          stop("Input must be a matrix. Got: ", class(x)[1])
        }
    if (!is.numeric(x)) {
          stop("Matrix must be numeric. Got: ", typeof(x))
        }
    if (nrow(x) < 2 || ncol(x) < 1) {
          stop("Matrix must have at least 2 rows and 1 column.")
        }
    if (any(is.na(x))) {
          warning("Input contains NA values; outlier detection may be unreliable.")
        }

    outliers <- array(TRUE, dim = dim(x))
    for (j in seq_len(ncol(x))) {
          outliers[, j] <- outliers[, j] & tukey.outlier(x[, j])
          # Changed && to & for element-wise comparison
        }
    outlier.vec <- logical(nrow(x))
    for (i in seq_len(nrow(x))) {
          outlier.vec[i] <- all(outliers[i, ])
        }
    outlier.vec
  }

# ---- Task 4: Validate the Fix --------------------------------
result_fixed <- corrected_tukey(test_mat)
cat("Result:", result_fixed, "\n")
cat("Length:", length(result_fixed), "\n")
cat("Class: ", class(result_fixed), "\n")

# ---- Edge-case tests -----------------------------------------
cat("\n=== Edge-Case Tests ===\n")

# Non-matrix input
tryCatch(corrected_tukey(data.frame(a = 1:5, b = 6:10)),
                  error = function(e) cat("PASS (data.frame):", conditionMessage(e), "\n"))

         # Non-numeric matrix
         tryCatch(corrected_tukey(matrix(letters[1:12], nrow = 3)),
                           error = function(e) cat("PASS (character):", conditionMessage(e), "\n"))

                  # Matrix with NAs
                  mat_na <- test_mat
                  mat_na[1, 1] <- NA
                  tryCatch(corrected_tukey(mat_na),
                                    warning = function(w) cat("PASS (NA warning):", conditionMessage(w), "\n"))

                           cat("\nDone.\n")
