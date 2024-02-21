package move_processed_files_to_cold_bucket_function

import (
	"context"
	"fmt"
	"log"
	"net/http"
	"time"

	"cloud.google.com/go/storage"
	"github.com/GoogleCloudPlatform/functions-framework-go/functions"
)

func init() {
	functions.HTTP("MoveProcessedFileToColdBucket", moveProcessedFilesToColdBucket)
}

func moveProcessedFilesToColdBucket(w http.ResponseWriter, r *http.Request) {
	rawSourceBucket := "event-driven-functions-qatar-fifa-world-cup-stats-raw-wf"
	rawSourceObject := "input/stats/world_cup_team_players_stats_raw_ndjson.json"
	domainSourceBucket := "event-driven-functions-qatar-fifa-world-cup-stats-wf"
	domainSourceObject := "input/stats/world_cup_team_players_stats_domain.json"

	DestBucket := "event-driven-qatar-fifa-world-cup-stats-cold"
	RawDestObject := "input/raw/world_cup_team_players_stats_raw_ndjson.json"
	DomainDestObject := "input/domain/world_cup_team_players_stats_domain.json"

	errMoveRawFileColdBucket := moveFile(
		rawSourceBucket,
		rawSourceObject,
		DestBucket,
		RawDestObject,
	)

	if errMoveRawFileColdBucket != nil {
		err := fmt.Sprintf("raw.moveFile: %w", errMoveRawFileColdBucket)

		log.Print(err)
		http.Error(w, err, http.StatusInternalServerError)

		return
	}

	errMoveDomainFileColdBucket := moveFile(
		domainSourceBucket,
		domainSourceObject,
		DestBucket,
		DomainDestObject,
	)

	if errMoveDomainFileColdBucket != nil {
		err := fmt.Sprintf("domain.moveFile: %w", errMoveDomainFileColdBucket)

		log.Print(err)
		http.Error(w, err, http.StatusInternalServerError)

		return
	}

	fmt.Fprintf(w, "OK")

	return
}

func moveFile(
	sourceBucket,
	sourceObject string,
	destBucket,
	destObject string) error {

	ctx := context.Background()
	client, err := storage.NewClient(ctx)
	if err != nil {
		return fmt.Errorf("storage.NewClient: %w", err)
	}
	defer client.Close()

	ctx, cancel := context.WithTimeout(ctx, time.Second*10)
	defer cancel()

	src := client.Bucket(sourceBucket).Object(sourceObject)
	dst := client.Bucket(destBucket).Object(destObject)

	if _, err := dst.CopierFrom(src).Run(ctx); err != nil {
		return fmt.Errorf("Object(%q).CopierFrom(%q).Run: %w", destObject, sourceObject, err)
	}
	if err := src.Delete(ctx); err != nil {
		return fmt.Errorf("Object(%q).Delete: %w", sourceObject, err)
	}
	log.Printf("Blob %v moved to %v.\n", sourceObject, destObject)
	return nil
}
