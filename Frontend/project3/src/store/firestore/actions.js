export const actions = {
  getDocumentReference: function(context, { collection, document }) {
    return context.state.db.collection(collection).doc(document)
  },
  getCollectionDocs: function(context, collection) {
    return context.state.db
      .collection(collection)
      .get()
      .then(docs => {
        return docs
      })
  },
  getTrainHistory: function(context, { trainId, startTime, endTime }) {
    return context.state.db
      .collection('history')
      .where('train', '==', trainId)
      .where('timestamp', '>', startTime)
      .where('timestamp', '<', endTime)
      .get()
      .then(docs => {
        return docs
      })
  }
}
