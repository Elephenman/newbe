#!/usr/bin/env Rscript
# CellChat细胞通讯一键分析
suppressPackageStartupMessages({
  if (!require(CellChat)) { cat("需要CellChat\n"); quit(status=1) }
  library(Seurat); library(ggplot2)
})
get_input <- function(p,d=NULL){v=readline(paste0(p," [默认: ",d,"]: "));if(v==""||is.null(v))return(d);return(v)}
cat("============================================================\n")
cat("  📡 CellChat细胞通讯\n")
cat("============================================================\n\n")
obj_path <- get_input("Seurat对象路径(rds)","seurat.rds")
species <- get_input("物种(human/mouse)","human")
db <- if(species=="human") CellChatDB.human else CellChatDB.mouse
obj <- readRDS(obj_path)
chat <- createCellChat(object = obj, group.by = "seurat_clusters")
chat <- setIdentDB(chat, db = db)
chat <- findOverExpressedGenes(chat)
chat <- findOverExpressedInteractions(chat)
chat <- computeCommunProb(chat)
chat <- filterCommunication(chat, min.cells = 10)
chat <- computeCommunProbPathway(chat)
chat <- aggregateNet(chat)

# 绘图
p1 <- netVisual_circle(chat@net$count, vertex.weight = chat@net$count.sum)
ggsave("cellchat_network.png", p1, width=10, height=8, dpi=300)
p2 <- netVisual_signaling_role(chat, width=12, height=6)
ggsave("cellchat_signaling.png", p2, width=12, height=6, dpi=300)

# 保存结果
lr <- subsetCommunication(chat); write.csv(lr, "cellchat_LR_interactions.csv", row.names=FALSE)
cat("✅ CellChat分析完成\n")
cat("   LR互作数:", nrow(lr), "\n")