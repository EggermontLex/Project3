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
  getTrainHistory: function(context, { trainId, hours }) {
    let d = new Date()
    d = new Date(d.setHours(d.getHours() - hours))
    return context.state.db
      .collection('history')
      .where('train', '==', trainId)
      .where('timestamp', '>', d)
      .get()
      .then(docs => {
        return docs
      })
  }
}
