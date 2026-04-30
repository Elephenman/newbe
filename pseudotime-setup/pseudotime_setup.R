#!/usr/bin/env Rscript
# 拟时序分析启动器(Monocle3/Slingshot)

get_input <- function(p, d=NULL) {
  v <- readline(paste0(p, " [默认: ", d, "]: "))
  if (v == "" || is.null(v)) return(d)
  return(v)
}

cat("============================================================\n")
cat("  拟时序分析启动器\n")
cat("============================================================\n\n")

obj_path <- get_input("Seurat对象路径(rds)", "seurat.rds")
root <- get_input("root定义(cluster号/基因名)", "3")
method <- get_input("轨迹方法(monocle3/slingshot)", "monocle3")

# 验证输入文件
if (!file.exists(obj_path)) {
  cat("[ERROR] File not found:", obj_path, "\n")
  cat("Expected: Seurat .rds object\n")
  quit(status=1)
}

cat("[Processing] Loading Seurat object...\n")
obj <- readRDS(obj_path)

# 验证Seurat对象
if (!inherits(obj, "Seurat")) {
  cat("[ERROR] Object is not a Seurat object. Got class:", class(obj), "\n")
  quit(status=1)
}

cat("[Processing] Object loaded:", ncol(obj), "cells,", nrow(obj), "features\n")

# 检查是否有UMAP
if (!"umap" %in% names(obj@reductions) && !"UMAP" %in% names(obj@reductions)) {
  cat("[ERROR] No UMAP reduction found. Run RunUMAP first.\n")
  quit(status=1)
}

suppressPackageStartupMessages({
  if (method == "monocle3") {
    if (!require(monocle3)) {
      cat("[ERROR] monocle3 not installed. Install with:\n")
      cat("  BiocManager::install('monocle3')\n")
      quit(status=1)
    }

    cat("[Processing] Converting to cell_data_set...\n")

    # Convert Seurat to cell_data_set
    # Try SeuratWrappers first, fall back to manual conversion
    cds <- tryCatch({
      if (require(SeuratWrappers)) {
        as.cell_data_set(obj)
      } else {
        cat("[INFO] SeuratWrappers not found, using manual conversion...\n")

        # Manual conversion
        require(Seurat)
        umap_coords <- Embeddings(obj, reduction = "umap")
        pca_coords <- Embeddings(obj, reduction = "pca")[, 1:min(30, ncol(Embeddings(obj, reduction = "pca")))]

        # Create cell_data_set
        expr_matrix <- GetAssayData(obj, slot = "data")
        cds <- monocle3::new_cell_data_set(
          expression_data = expr_matrix,
          cell_metadata = obj@meta.data,
          gene_metadata = data.frame(gene_short_name = rownames(expr_matrix), row.names = rownames(expr_matrix))
        )

        # Set UMAP and PCA reductions
        monocle3::reducedDims(cds)[["UMAP"]] <- umap_coords
        monocle3::reducedDims(cds)[["PCA"]] <- pca_coords

        cds
      }
    }, error = function(e) {
      cat("[ERROR] Conversion failed:", e$message, "\n")
      quit(status=1)
    })

    cat("[Processing] Learning graph...\n")
    cds <- monocle3::learn_graph(cds)

    # Set root cells
    cat("[Processing] Setting root cells (cluster =", root, ")...\n")
    root_cells <- tryCatch({
      if (root %in% as.character(obj@meta.data$seurat_clusters)) {
        colnames(cds)[obj@meta.data$seurat_clusters == root]
      } else {
        # Try as a column name
        root_cells <- colnames(cds)[1:min(10, ncol(cds))]
        cat("[WARN] Could not find cluster", root, ", using first cells as root\n")
        root_cells
      }
    }, error = function(e) {
      colnames(cds)[1:min(10, ncol(cds))]
    })

    if (length(root_cells) == 0) {
      cat("[ERROR] No root cells found\n")
      quit(status=1)
    }

    cds <- monocle3::order_cells(cds, root_cells = root_cells[1])

    # Plot
    p <- monocle3::plot_cells(cds, color_cells_by = "pseudotime")
    ggsave("pseudotime_monocle3.png", p, width=10, height=8, dpi=300)

    # Save pseudotime values
    pt <- monocle3::pseudotime(cds)
    write.csv(data.frame(cell=names(pt), pseudotime=as.numeric(pt)),
              "pseudotime_coords.csv", row.names=FALSE)

    cat("[Done] Pseudotime analysis (Monocle3) complete\n")
    cat("  Plot: pseudotime_monocle3.png\n")
    cat("  Data: pseudotime_coords.csv\n")

  } else {
    # Slingshot
    if (!require(slingshot)) {
      cat("[ERROR] slingshot not installed. Install with:\n")
      cat("  BiocManager::install('slingshot')\n")
      quit(status=1)
    }

    cat("[Processing] Running Slingshot...\n")
    require(SingleCellExperiment)

    rd <- Embeddings(obj, reduction = "umap")
    cl <- obj@meta.data$seurat_clusters

    sce <- slingshot::slingshot(SingleCellExperiment(
      reducedDims = list(UMAP = rd)
    ), clusterLabels = cl, start.clus = root)

    pt <- slingshot::slingPseudotime(sce)

    # Plot
    png("pseudotime_slingshot.png", width=800, height=600)
    plot(rd, col = pt[,1], pch = 16, xlab = "UMAP1", ylab = "UMAP2",
         main = "Slingshot Pseudotime")
    dev.off()

    # Save
    write.csv(data.frame(cell = rownames(rd), pseudotime = pt[,1]),
              "pseudotime_coords.csv", row.names = FALSE)

    cat("[Done] Pseudotime analysis (Slingshot) complete\n")
    cat("  Plot: pseudotime_slingshot.png\n")
    cat("  Data: pseudotime_coords.csv\n")
  }
})
